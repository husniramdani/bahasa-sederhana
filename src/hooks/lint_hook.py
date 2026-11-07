#!/usr/bin/env python3
"""Hook pemeriksaan berkas dan hook pemeriksaan balasan untuk Bahasa Sederhana.

Satu skrip melayani dua peristiwa hook Claude Code. Nama peristiwa dibaca dari
`hook_event_name` di JSON pada stdin.

PostToolUse (alat Write, Edit, atau MultiEdit):
    Memeriksa berkas .md, .mdx, .txt, atau .rst yang baru ditulis dengan
    evals/bahasa_lint.py. Jika ada pelanggaran, skrip mencetak
    {"decision": "block", "reason": "..."} agar agen memperbaiki berkas itu.

Stop:
    Membaca balasan terakhir agen dari transkrip, lalu menghitung format dan
    basa-basi yang terlihat pembaca. Hook ini juga mendaftar istilah Inggris
    yang belum miring dan padanan Indonesia yang janggal. Jika ada temuan,
    skrip mencetak {"systemMessage": "..."}. Panjang balasan tidak dibatasi.

Pengecualian path:
    BAHASA_SEDERHANA_LINT_EXCLUDE berisi pola glob yang dipisah koma atau titik
    dua, misalnya "docs/lama/*,*.txt". Pola "*" mematikan pemeriksaan berkas.

Skrip ini tidak pernah gagal. Jika terjadi kesalahan apa pun, skrip keluar
dengan kode 0 tanpa keluaran.

Hanya pustaka standar Python 3.
"""

import fnmatch
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EVALS = os.path.normpath(os.path.join(HERE, "..", "..", "evals"))

TEXT_EXTENSIONS = (".md", ".mdx", ".txt", ".rst")
FILE_TOOLS = ("Write", "Edit", "MultiEdit")
EXCLUDE_ENV = "BAHASA_SEDERHANA_LINT_EXCLUDE"
EXCLUDED_DIRS = (".git", "node_modules", ".claude")
# Berkas ini berisi contoh buruk yang disengaja.
EXCLUDED_FRAGMENTS = ("skills/bahasa-sederhana/", "examples/sebelum-sesudah.md", "prompts/system-prompt.md", "output-styles/bahasa-sederhana.md")
MAX_DETAIL_LINES = 10
MAX_TERMS = 5

PROCEDURAL_HINT = re.compile(
    r"runbook|panduan|memulai|install|instal|pemasangan|troubleshoot|pemecahan|prosedur"
    r"|quickstart|getting[-_ ]?started|langkah",
    re.IGNORECASE,
)

READER_LABELS = (
    ("tanda_pisah", "tanda pisah"),
    ("huruf_tebal", "huruf tebal"),
    ("subjudul", "subjudul"),
    ("butir", "baris butir"),
    ("kata_cakapan", "kata cakapan"),
    ("pembuka", "pembuka basa-basi"),
    ("penutup", "penutup basa-basi"),
)


def _linter():
    if EVALS not in sys.path:
        sys.path.insert(0, EVALS)
    import bahasa_lint  # noqa: E402

    return bahasa_lint


# ---------------------------------------------------------------------------
# PostToolUse


def _exclude_patterns():
    raw = os.environ.get(EXCLUDE_ENV, "")
    return [p.strip() for p in re.split(r"[,:]", raw) if p.strip()]


def is_excluded(path, cwd=None):
    full = os.path.abspath(path).replace(os.sep, "/")
    parts = full.split("/")
    if any(d in parts[:-1] for d in EXCLUDED_DIRS):
        return True
    if any(fragment in full for fragment in EXCLUDED_FRAGMENTS):
        return True
    candidates = {full, os.path.basename(full)}
    if cwd:
        try:
            rel = os.path.relpath(full, os.path.abspath(cwd)).replace(os.sep, "/")
            if not rel.startswith(".."):
                candidates.add(rel)
        except ValueError:
            pass
    for pattern in _exclude_patterns():
        pattern = pattern.replace(os.sep, "/")
        for candidate in candidates:
            if fnmatch.fnmatch(candidate, pattern) or fnmatch.fnmatch(candidate, "*/" + pattern):
                return True
    return False


def guess_type(path, text):
    if PROCEDURAL_HINT.search(os.path.basename(path)):
        return "procedural"
    for line in text.splitlines():
        m = re.match(r"^\s{0,3}#\s+(.+)$", line)
        if m:
            return "procedural" if PROCEDURAL_HINT.search(m.group(1)) else "descriptive"
    return "descriptive"


def handle_post_tool_use(payload):
    if payload.get("tool_name") not in FILE_TOOLS:
        return None
    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path")
    if not isinstance(path, str) or not path:
        return None
    cwd = payload.get("cwd") if isinstance(payload.get("cwd"), str) else None
    if not os.path.isabs(path) and cwd:
        path = os.path.join(cwd, path)
    if not path.lower().endswith(TEXT_EXTENSIONS):
        return None
    if is_excluded(path, cwd):
        return None
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    lint = _linter()
    details = lint.lint_detail(text, guess_type(path, text))
    if not details:
        return None

    shown = path
    if cwd:
        rel = os.path.relpath(os.path.abspath(path), os.path.abspath(cwd))
        if not rel.startswith(".."):
            shown = rel
    lines = ["bahasa-sederhana: %s punya %d pelanggaran." % (shown, len(details))]
    for d in details[:MAX_DETAIL_LINES]:
        lines.append("baris %d, %s: %s" % (d["line"], d["category"], d["text"]))
    lines.append("Perbaiki temuan ini di berkas yang baru Anda tulis, lalu lanjutkan.")
    return {"decision": "block", "reason": "\n".join(lines)}


# ---------------------------------------------------------------------------
# Stop


def _content_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n\n".join(p for p in parts if p.strip())
    return ""


def last_assistant_text(transcript_path):
    """Kembalikan teks pesan asisten terakhir dari transkrip JSONL."""
    entries = []
    with open(transcript_path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                obj = json.loads(raw)
            except ValueError:
                continue
            if not isinstance(obj, dict):
                continue
            message = obj.get("message") if isinstance(obj.get("message"), dict) else {}
            role = message.get("role") or obj.get("role") or obj.get("type")
            content = message.get("content", obj.get("content"))
            entries.append((role, message.get("id"), _content_text(content)))

    index = len(entries) - 1
    while index >= 0 and not (entries[index][0] == "assistant" and entries[index][2].strip()):
        index -= 1
    if index < 0:
        return ""
    message_id = entries[index][1]
    texts = [entries[index][2]]
    # Satu pesan dapat tersimpan sebagai beberapa baris dengan id yang sama.
    j = index - 1
    while message_id and j >= 0 and entries[j][0] == "assistant" and entries[j][1] == message_id:
        if entries[j][2].strip():
            texts.insert(0, entries[j][2])
        j -= 1
    return "\n\n".join(texts)


def handle_stop(payload):
    if payload.get("stop_hook_active") is True:
        return None
    transcript = payload.get("transcript_path")
    if not isinstance(transcript, str) or not os.path.isfile(transcript):
        return None
    text = last_assistant_text(transcript)
    if not text.strip():
        return None

    lint = _linter()
    counts = lint.reader_check(text)
    findings = []
    for key, label in READER_LABELS:
        n = counts.get(key, 0)
        if n:
            findings.append("%d %s" % (n, label))

    details = lint.lint_detail(text, "reply")
    tegak = _distinct_terms(details, "istilah_tegak")
    janggal = _distinct_terms(details, "padanan_janggal")

    parts = []
    if findings:
        parts.append(", ".join(findings))
    if tegak:
        parts.append("kata Inggris belum miring: " + tegak)
    if janggal:
        parts.append("padanan janggal: " + janggal)
    if not parts:
        return None
    parts = [parts[0]] + [p[0].upper() + p[1:] for p in parts[1:]]
    advice = []
    if tegak:
        advice.append("Tulis istilah Inggris dengan huruf miring, misalnya *output*.")
    if janggal:
        advice.append("Pakai istilah Inggris yang lazim dengan huruf miring.")
    if findings:
        advice.append("Jawab dalam bentuk prosa.")
    message = "bahasa-sederhana cek balasan: %s. %s" % (". ".join(parts), " ".join(advice))
    return {"systemMessage": message}


def _distinct_terms(details, category):
    """Gabungkan paling banyak MAX_TERMS istilah berbeda dari satu kategori."""
    terms = []
    for d in details:
        if d["category"] != category:
            continue
        term = d["text"].lower()
        if term not in terms:
            terms.append(term)
    if not terms:
        return ""
    shown = ", ".join(terms[:MAX_TERMS])
    if len(terms) > MAX_TERMS:
        shown += ", dan %d lainnya" % (len(terms) - MAX_TERMS)
    return shown


# ---------------------------------------------------------------------------


def main():
    raw = sys.stdin.read()
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        return None
    event = payload.get("hook_event_name")
    if event == "PostToolUse":
        return handle_post_tool_use(payload)
    if event == "Stop":
        return handle_stop(payload)
    return None


if __name__ == "__main__":
    try:
        result = main()
        if result:
            sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - hook tidak boleh menghentikan sesi
        pass
    sys.exit(0)
