#!/usr/bin/env python3
"""Benchmark balasan obrolan untuk Bahasa Sederhana.

Skrip ini menjalankan setiap skenario di evals/reply_scenarios.json dengan
Claude Code CLI. Kelompok "dasar" tidak mendapat prompt tambahan. Setiap
`--skill NAMA=PATH` menambah satu kelompok yang mendapat isi PATH lewat
`--append-system-prompt`.

Isi PATH dibaca dengan aturan ini:

- Berkas .md yang diawali frontmatter (baris pertama `---`), misalnya SKILL.md:
  isi setelah frontmatter.
- Berkas .md lain dengan dua baris `---`, misalnya prompts/system-prompt.md:
  blok di antara dua baris itu.
- Berkas lain: seluruh isinya.

Setiap balasan dinilai dengan `reader_check` dari evals/bahasa_lint.py. Skrip ini
juga memeriksa apakah istilah skenario dijelaskan dalam kurung pada pemakaian
pertama, misalnya "CORS (aturan browser tentang ...)".

Pemakaian:

    python3 evals/run_reply_bench.py \\
        --skill bahasa-sederhana=prompts/system-prompt.md \\
        --out evals/results/balasan

Keluaran: DIR/raw/<kelompok>/<id>.md, DIR/summary.json, dan DIR/report.md.

Syarat: Claude Code CLI ada di PATH dan sudah masuk. Jangan pasang plugin
bahasa-sederhana saat benchmark berjalan, karena hook-nya ikut memengaruhi
kelompok dasar. Skrip ini tidak berisi hasil. Hanya pustaka standar Python 3.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import bahasa_lint  # noqa: E402

SCENARIOS = os.path.join(HERE, "reply_scenarios.json")
DEFAULT_MODEL = "claude-sonnet-5-5"
BASELINE = "dasar"
TIMEOUT_SECONDS = 600
TERM_WINDOW = 30


def load_scenarios():
    with open(SCENARIOS, encoding="utf-8") as fh:
        return json.load(fh)


def read_prompt_file(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read().replace("\r\n", "\n")
    if not path.lower().endswith(".md"):
        return text.strip()
    lines = text.split("\n")
    marks = [i for i, line in enumerate(lines) if line.strip() == "---"]
    if lines and lines[0].strip() == "---" and len(marks) >= 2:
        return "\n".join(lines[marks[1] + 1:]).strip()
    if len(marks) >= 2:
        return "\n".join(lines[marks[0] + 1: marks[1]]).strip()
    return text.strip()


def parse_skill(value):
    if "=" not in value:
        raise argparse.ArgumentTypeError("format --skill adalah NAMA=PATH")
    name, path = value.split("=", 1)
    name = name.strip()
    if not re.fullmatch(r"[\w.-]+", name) or name == BASELINE:
        raise argparse.ArgumentTypeError("nama kelompok tidak valid: %r" % name)
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError("berkas tidak ditemukan: %s" % path)
    return name, path


def require_cli():
    if shutil.which("claude") is None:
        print(
            "Kesalahan: perintah `claude` tidak ditemukan di PATH. "
            "Pasang Claude Code CLI dan masuk dulu. Lalu, jalankan skrip ini lagi.",
            file=sys.stderr,
        )
        sys.exit(1)


def run_claude(prompt, model, system_append=None):
    cmd = ["claude", "-p", prompt, "--model", model]
    if system_append:
        cmd += ["--append-system-prompt", system_append]
    workdir = tempfile.mkdtemp(prefix="bahasa-sederhana-balasan-")
    try:
        proc = subprocess.run(
            cmd,
            cwd=workdir,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip()[-400:]
        raise RuntimeError("kode keluar %d: %s" % (proc.returncode, tail))
    return proc.stdout


def term_explained(text, term):
    """Benar jika kurung buka muncul tidak jauh setelah pemakaian pertama istilah itu."""
    m = re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.IGNORECASE)
    if not m:
        return False
    tail = text[m.end(): m.end() + TERM_WINDOW + 1]
    return re.match(r"[^\n.!?()]{0,%d}\(" % TERM_WINDOW, tail) is not None


def _fmt(value, digits=2):
    return ("%.*f" % (digits, value)).replace(".", ",")


def summarize(arms, scenarios, out_dir, model):
    summary = {"model": model, "arms": {}}
    for arm in arms:
        rows = {}
        for scenario in scenarios:
            path = os.path.join(out_dir, "raw", arm, scenario["id"] + ".md")
            if not os.path.isfile(path):
                continue
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            row = bahasa_lint.reader_check(text)
            row["term_explained"] = term_explained(text, scenario["term"])
            rows[scenario["id"]] = row
        n = len(rows)
        totals = {k: sum(r[k] for r in rows.values()) for k in bahasa_lint.READER_KEYS}
        summary["arms"][arm] = {
            "replies": n,
            "visible_total": sum(r["visible_total"] for r in rows.values()),
            "visible_mean": round(sum(r["visible_total"] for r in rows.values()) / n, 2) if n else None,
            "term_explained": sum(1 for r in rows.values() if r["term_explained"]),
            "totals": totals,
            "scenarios": rows,
        }
    return summary


def write_report(summary, out_dir):
    out = [
        "# Laporan benchmark balasan Bahasa Sederhana",
        "",
        "Laporan ini dibuat oleh `evals/run_reply_bench.py` untuk model `%s`. "
        "Setiap balasan dinilai dengan `reader_check` dari `evals/bahasa_lint.py`." % summary["model"],
        "",
        "Kolom format menghitung tanda pisah, huruf tebal, subjudul, baris butir, kata cakapan, pembuka, dan penutup. "
        "Kolom istilah menghitung balasan yang menjelaskan istilah skenario dalam kurung pada pemakaian pertama.",
        "",
        "| Kelompok | Balasan | Temuan format (rata-rata) | Istilah dijelaskan |",
        "|---|---|---|---|",
    ]
    for arm, data in summary["arms"].items():
        if not data["replies"]:
            out.append("| %s | 0 | belum ada | belum ada |" % arm)
            continue
        out.append("| %s | %d | %s | %d dari %d |" % (
            arm, data["replies"], _fmt(data["visible_mean"]), data["term_explained"], data["replies"]))
    arms = list(summary["arms"])
    out += ["", "Temuan per jenis, dijumlahkan untuk semua balasan:", ""]
    out.append("| Jenis | " + " | ".join(arms) + " |")
    out.append("|---|" + "---|" * len(arms))
    for key in bahasa_lint.READER_KEYS:
        out.append("| %s | %s |" % (key, " | ".join(str(summary["arms"][a]["totals"][key]) for a in arms)))
    with open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Benchmark balasan obrolan Bahasa Sederhana dengan Claude Code CLI.")
    parser.add_argument("--skill", action="append", type=parse_skill, default=[], metavar="NAMA=PATH",
                        help="tambah satu kelompok dengan prompt dari PATH (dapat diulang)")
    parser.add_argument("--out", required=True, metavar="DIR", help="direktori keluaran")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="model Claude (bawaan: %s)" % DEFAULT_MODEL)
    args = parser.parse_args(argv)

    names = [name for name, _ in args.skill]
    if len(set(names)) != len(names):
        parser.error("nama kelompok --skill harus unik")

    require_cli()
    scenarios = load_scenarios()
    arms = [(BASELINE, None)] + [(name, read_prompt_file(path)) for name, path in args.skill]

    failures = 0
    total = len(arms) * len(scenarios)
    done = 0
    for scenario in scenarios:
        for arm, prompt in arms:
            done += 1
            print("[%d/%d] %s, %s" % (done, total, arm, scenario["id"]), flush=True)
            try:
                text = run_claude(scenario["prompt"], args.model, prompt)
            except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
                failures += 1
                print("  gagal: %s" % exc, file=sys.stderr)
                continue
            path = os.path.join(args.out, "raw", arm, scenario["id"] + ".md")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)

    os.makedirs(args.out, exist_ok=True)
    summary = summarize([a for a, _ in arms], scenarios, args.out, args.model)
    with open(os.path.join(args.out, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    write_report(summary, args.out)
    print("Ringkasan ditulis ke %s dan %s." % (
        os.path.join(args.out, "summary.json"), os.path.join(args.out, "report.md")))
    if failures:
        print("%d panggilan gagal. Lihat pesan di atas." % failures, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
