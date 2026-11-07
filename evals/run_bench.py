#!/usr/bin/env python3
"""Benchmark dokumen untuk Bahasa Sederhana.

Untuk setiap skenario di evals/scenarios.json dan setiap model, skrip ini
menjalankan Claude Code CLI dua kali:

- tanpa-skill: `claude -p PROMPT --model MODEL`
- dengan-skill: perintah yang sama dengan `--append-system-prompt`, berisi
  isi SKILL.md tanpa frontmatter

Setiap jawaban disimpan di evals/results/raw/<model>/<kelompok>/<id>.md.
Lalu, setiap jawaban diperiksa dengan evals/bahasa_lint.py memakai jenis teks
dari skenarionya. Ringkasannya ditulis ke evals/results/report.md.

Pemakaian:

    python3 evals/run_bench.py              # semua model, semua skenario
    python3 evals/run_bench.py --smoke      # claude-sonnet-5-5, dua skenario pertama
    python3 evals/run_bench.py --report-only

Syarat: Claude Code CLI ada di PATH dan sudah masuk. Jangan pasang plugin
bahasa-sederhana saat benchmark berjalan. Hook sesinya akan memuat aturan ke
kelompok tanpa-skill. Setiap panggilan berjalan di direktori sementara agar
CLAUDE.md dan pengaturan proyek tidak ikut terbaca.

Skrip ini tidak berisi hasil. Semua angka di laporan dihitung dari berkas
mentah. Hanya pustaka standar Python 3.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import bahasa_lint  # noqa: E402

SCENARIOS = os.path.join(HERE, "scenarios.json")
SKILL = os.path.join(ROOT, "skills", "bahasa-sederhana", "SKILL.md")
RESULTS = os.path.join(HERE, "results")
RAW = os.path.join(RESULTS, "raw")
REPORT = os.path.join(RESULTS, "report.md")

MODELS = ["claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5", "claude-fable-5-1"]
SMOKE_MODEL = "claude-sonnet-5-5"
SMOKE_COUNT = 2
ARMS = ("tanpa-skill", "dengan-skill")
TIMEOUT_SECONDS = 900


def load_scenarios():
    with open(SCENARIOS, encoding="utf-8") as fh:
        return json.load(fh)


def skill_body():
    with open(SKILL, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.replace("\r\n", "\n").split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:]).strip()
    return text.strip()


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
    workdir = tempfile.mkdtemp(prefix="bahasa-sederhana-bench-")
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


def raw_path(model, arm, scenario_id):
    return os.path.join(RAW, model, arm, scenario_id + ".md")


def run_all(models, scenarios):
    body = skill_body()
    failures = 0
    total = len(models) * len(scenarios) * len(ARMS)
    done = 0
    for model in models:
        for scenario in scenarios:
            for arm in ARMS:
                done += 1
                print("[%d/%d] %s, %s, %s" % (done, total, model, arm, scenario["id"]), flush=True)
                try:
                    text = run_claude(scenario["prompt"], model, body if arm == "dengan-skill" else None)
                except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
                    failures += 1
                    print("  gagal: %s" % exc, file=sys.stderr)
                    continue
                path = raw_path(model, arm, scenario["id"])
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(text)
    return failures


def _fmt(value, digits=2):
    return ("%.*f" % (digits, value)).replace(".", ",")


def collect(scenarios):
    """Kembalikan {model: {arm: [hasil lint]}} dari berkas mentah."""
    types = {s["id"]: s["type"] for s in scenarios}
    data = {}
    if not os.path.isdir(RAW):
        return data
    for model in sorted(os.listdir(RAW)):
        model_dir = os.path.join(RAW, model)
        if not os.path.isdir(model_dir):
            continue
        for arm in ARMS:
            arm_dir = os.path.join(model_dir, arm)
            if not os.path.isdir(arm_dir):
                continue
            for name in sorted(os.listdir(arm_dir)):
                scenario_id, ext = os.path.splitext(name)
                if ext != ".md" or scenario_id not in types:
                    continue
                with open(os.path.join(arm_dir, name), encoding="utf-8") as fh:
                    result = bahasa_lint.lint(fh.read(), types[scenario_id])
                result["id"] = scenario_id
                data.setdefault(model, {}).setdefault(arm, []).append(result)
    return data


def build_report(scenarios):
    data = collect(scenarios)
    if not data:
        return None
    out = [
        "# Laporan benchmark Bahasa Sederhana",
        "",
        "Laporan ini dibuat oleh `evals/run_bench.py` dari berkas di `evals/results/raw/`. "
        "Setiap jawaban diperiksa dengan `evals/bahasa_lint.py` memakai jenis teks dari skenarionya. "
        "Kelompok tanpa-skill tidak mendapat aturan. Kelompok dengan-skill mendapat isi `SKILL.md` di prompt sistem.",
        "",
        "Linter ini membaca pola, bukan makna. Pakai angka ini untuk membandingkan dua kelompok, bukan sebagai bukti kepatuhan.",
    ]
    for model in sorted(data):
        out += [
            "",
            "## %s" % model,
            "",
            "| Kelompok | Jawaban | Pelanggaran per 100 kata (rata-rata) | Kalimat terpanjang (rata-rata kata) |",
            "|---|---|---|---|",
        ]
        for arm in ARMS:
            results = data[model].get(arm, [])
            if not results:
                out.append("| %s | 0 | belum ada | belum ada |" % arm)
                continue
            n = len(results)
            per100 = sum(r["violations_per_100w"] for r in results) / n
            longest = sum(r["longest_sentence_words"] for r in results) / n
            out.append("| %s | %d | %s | %s |" % (arm, n, _fmt(per100), _fmt(longest, 1)))
        out += ["", "Pelanggaran per kategori, dijumlahkan untuk semua jawaban:", ""]
        out.append("| Kategori | " + " | ".join(ARMS) + " |")
        out.append("|---|" + "---|" * len(ARMS))
        for category in bahasa_lint.CATEGORIES:
            cells = []
            for arm in ARMS:
                results = data[model].get(arm, [])
                cells.append(str(sum(r["violations"][category] for r in results)))
            out.append("| %s | %s |" % (category, " | ".join(cells)))
    os.makedirs(RESULTS, exist_ok=True)
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return REPORT


def main(argv=None):
    parser = argparse.ArgumentParser(description="Benchmark dokumen Bahasa Sederhana dengan Claude Code CLI.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--smoke", action="store_true", help="jalankan %s pada dua skenario pertama" % SMOKE_MODEL)
    group.add_argument("--report-only", action="store_true", help="buat ulang laporan dari berkas mentah saja")
    args = parser.parse_args(argv)

    scenarios = load_scenarios()

    failures = 0
    if not args.report_only:
        require_cli()
        if args.smoke:
            failures = run_all([SMOKE_MODEL], scenarios[:SMOKE_COUNT])
        else:
            failures = run_all(MODELS, scenarios)

    path = build_report(scenarios)
    if path is None:
        print("Belum ada berkas mentah di %s. Laporan tidak ditulis." % os.path.relpath(RAW, ROOT))
        return 1 if failures else 0
    print("Laporan ditulis ke %s." % os.path.relpath(path, ROOT))
    if failures:
        print("%d panggilan gagal. Lihat pesan di atas." % failures, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
