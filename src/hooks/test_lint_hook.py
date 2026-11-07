#!/usr/bin/env python3
"""Pengujian lint_hook.py. Jalankan dengan: python3 src/hooks/test_lint_hook.py

Setiap uji yang lulus mencetak "ok <nama uji>". Skrip keluar dengan kode 1
jika ada uji yang gagal. Hanya pustaka standar Python 3.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "lint_hook.py")

DIRTY_DOC = (
    "# Catatan kirimlog\n\n"
    "kirimlog adalah merupakan tool yg dirancang untuk mengirim log secara mulus; "
    "kamu sebaiknya cek config dulu — dll.\n\n"
    "Jika gagal, verifikasi port 9200 di server di mana anda memasang kirimlog, gak usah panik.\n"
)
CLEAN_DOC = (
    "# Catatan kirimlog\n\n"
    "Alat kirimlog membaca berkas log aplikasi dan mengirim isinya ke OpenSearch.\n\n"
    "Versi 3.0 memakai memori 25% lebih sedikit daripada versi sebelumnya.\n"
)
LONG_SENTENCE = (
    "Pengirim di kirimlog mengirim setiap kelompok log ke OpenSearch dengan bulk API "
    "lalu mencoba lagi tiga kali jika OpenSearch menolak kelompok itu karena beban tinggi.\n"
)
DIRTY_REPLY = (
    "Tentu! Ini penyebabnya.\n\n## Penyebab\n\n"
    "- **Port 9200** tertutup — OpenSearch belum jalan\n"
    "- Kata sandi salah, jadi muncul 401 aja\n\n"
    "Semoga membantu!"
)
CLEAN_REPLY = (
    "OpenSearch menolak kata sandi pengguna `kirimlog`, jadi kirimlog berhenti dengan HTTP 401. "
    "Isi `password` di `kirimlog.toml` dengan nilai yang benar. Lalu, jalankan kirimlog lagi."
)

TMP = tempfile.mkdtemp(prefix="bahasa-sederhana-hook-")


def run(payload, env=None, raw=None):
    full_env = dict(os.environ)
    full_env.pop("BAHASA_SEDERHANA_LINT_EXCLUDE", None)
    if env:
        full_env.update(env)
    data = raw if raw is not None else json.dumps(payload)
    proc = subprocess.run(
        [sys.executable, HOOK],
        input=data,
        capture_output=True,
        text=True,
        env=full_env,
        timeout=30,
    )
    assert proc.returncode == 0, "kode keluar %r, stderr %r" % (proc.returncode, proc.stderr)
    assert proc.stderr == "", "stderr tidak kosong: %r" % proc.stderr
    return proc.stdout


def write(rel, content):
    path = os.path.join(TMP, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def post(path, tool="Write", cwd=TMP):
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": tool,
        "tool_input": {"file_path": path, "content": "x"},
        "cwd": cwd,
    }


def transcript(messages):
    path = os.path.join(TMP, "transkrip-%d.jsonl" % len(os.listdir(TMP)))
    with open(path, "w", encoding="utf-8") as fh:
        for role, content, mid in messages:
            entry = {"type": role, "message": {"role": role, "content": content}}
            if mid:
                entry["message"]["id"] = mid
            fh.write(json.dumps(entry) + "\n")
    return path


def stop(path, active=False):
    return {
        "hook_event_name": "Stop",
        "transcript_path": path,
        "stop_hook_active": active,
        "cwd": TMP,
    }


def blocked(out):
    data = json.loads(out)
    assert data["decision"] == "block"
    return data["reason"]


# ---------------------------------------------------------------------------
# PostToolUse


def test_post_dirty_md_blocks():
    reason = blocked(run(post(write("catatan.md", DIRTY_DOC))))
    assert reason.startswith("bahasa-sederhana: catatan.md punya "), reason


def test_post_reason_format():
    reason = blocked(run(post(write("format.md", DIRTY_DOC))))
    lines = reason.split("\n")
    assert lines[0].endswith(" pelanggaran."), lines[0]
    assert lines[-1] == "Perbaiki temuan ini di berkas yang baru Anda tulis, lalu lanjutkan.", lines[-1]
    middle = lines[1:-1]
    assert 1 <= len(middle) <= 10, len(middle)
    for line in middle:
        assert line.startswith("baris "), line
        assert ", " in line and ": " in line, line
    total = int(lines[0].split(" punya ")[1].split()[0])
    assert total > 10 and len(middle) == 10, (total, len(middle))


def test_post_clean_md_silent():
    assert run(post(write("bersih.md", CLEAN_DOC))) == ""


def test_post_edit_tool_linted():
    reason = blocked(run(post(write("edit.md", DIRTY_DOC), tool="Edit")))
    assert "pelanggaran" in reason


def test_post_other_tool_silent():
    assert run(post(write("baca.md", DIRTY_DOC), tool="Read")) == ""


def test_post_txt_rst_mdx_linted():
    for name in ("catatan.txt", "catatan.rst", "catatan.mdx"):
        reason = blocked(run(post(write(name, DIRTY_DOC))))
        assert name in reason.split("\n")[0], reason


def test_post_code_file_silent():
    assert run(post(write("skrip.py", "# yg sebaiknya; dll\n"))) == ""
    assert run(post(write("data.json", '{"a": "yg sebaiknya"}'))) == ""


def test_post_relative_path():
    write("relatif/catatan.md", DIRTY_DOC)
    reason = blocked(run(post("relatif/catatan.md")))
    assert "relatif/catatan.md" in reason.split("\n")[0], reason


def test_post_missing_file_silent():
    assert run(post(os.path.join(TMP, "tidak-ada.md"))) == ""


def test_post_default_excludes():
    for rel in (
        ".git/catatan.md",
        "node_modules/paket/README.md",
        ".claude/catatan.md",
        "skills/bahasa-sederhana/SKILL.md",
        "skills/bahasa-sederhana/references/katalog-aturan.md",
        "examples/sebelum-sesudah.md",
    ):
        assert run(post(write(rel, DIRTY_DOC))) == "", rel


def test_post_env_exclude_glob():
    path = write("docs/lama/catatan.md", DIRTY_DOC)
    assert run(post(path), env={"BAHASA_SEDERHANA_LINT_EXCLUDE": "docs/lama/*"}) == ""
    assert run(post(path), env={"BAHASA_SEDERHANA_LINT_EXCLUDE": "docs/baru/*"}) != ""


def test_post_env_exclude_comma_and_colon():
    a = write("a/catatan.md", DIRTY_DOC)
    b = write("b/catatan.txt", DIRTY_DOC)
    env = {"BAHASA_SEDERHANA_LINT_EXCLUDE": "a/*, *.txt"}
    assert run(post(a), env=env) == ""
    assert run(post(b), env=env) == ""
    env = {"BAHASA_SEDERHANA_LINT_EXCLUDE": "a/*:*.txt"}
    assert run(post(a), env=env) == ""
    assert run(post(b), env=env) == ""


def test_post_env_exclude_everything():
    path = write("semua/catatan.md", DIRTY_DOC)
    assert run(post(path), env={"BAHASA_SEDERHANA_LINT_EXCLUDE": "*"}) == ""


def test_post_procedural_by_name():
    # Kalimat 23 kata: melanggar batas prosedur (20), tidak melanggar batas deskripsi (25).
    runbook = write("runbook-kirimlog.md", LONG_SENTENCE)
    catatan = write("arsitektur.md", LONG_SENTENCE)
    assert "kalimat_terlalu_panjang" in blocked(run(post(runbook)))
    assert run(post(catatan)) == ""


def test_post_procedural_by_heading():
    path = write("dok.md", "# Panduan memasang kirimlog\n\n" + LONG_SENTENCE)
    assert "kalimat_terlalu_panjang" in blocked(run(post(path)))


# ---------------------------------------------------------------------------
# Stop


def test_stop_dirty_reply_message():
    path = transcript([("user", "kenapa kirimlog gagal?", None), ("assistant", [{"type": "text", "text": DIRTY_REPLY}], "m1")])
    data = json.loads(run(stop(path)))
    message = data["systemMessage"]
    assert message.startswith("bahasa-sederhana cek balasan: "), message
    assert message.endswith(". Jawab dalam bentuk prosa."), message
    for label in ("tanda pisah", "huruf tebal", "subjudul", "baris butir", "kata cakapan", "pembuka", "penutup"):
        assert label in message, (label, message)


def test_stop_active_silent():
    path = transcript([("assistant", [{"type": "text", "text": DIRTY_REPLY}], "m1")])
    assert run(stop(path, active=True)) == ""


def test_stop_clean_reply_silent():
    path = transcript([("assistant", [{"type": "text", "text": CLEAN_REPLY}], "m1")])
    assert run(stop(path)) == ""


def test_stop_long_clean_reply_silent():
    long_reply = " ".join([CLEAN_REPLY] * 40)
    path = transcript([("assistant", [{"type": "text", "text": long_reply}], "m1")])
    assert run(stop(path)) == ""


def test_stop_english_opener_closer():
    text = "Sure, here is the fix. Restart kirimlog after editing kirimlog.toml. Hope this helps!"
    path = transcript([("assistant", [{"type": "text", "text": text}], "m1")])
    message = json.loads(run(stop(path)))["systemMessage"]
    assert "pembuka" in message and "penutup" in message, message


def test_stop_uses_last_assistant_message():
    path = transcript([
        ("assistant", [{"type": "text", "text": DIRTY_REPLY}], "m1"),
        ("user", "terima kasih", None),
        ("assistant", [{"type": "text", "text": CLEAN_REPLY}], "m2"),
        ("assistant", [{"type": "tool_use", "id": "t1", "name": "Read", "input": {}}], "m3"),
    ])
    assert run(stop(path)) == ""


def test_stop_joins_split_message():
    path = transcript([
        ("assistant", [{"type": "text", "text": "Tentu! Begini caranya."}], "m1"),
        ("assistant", [{"type": "tool_use", "id": "t1", "name": "Read", "input": {}}], "m1"),
        ("assistant", [{"type": "text", "text": CLEAN_REPLY}], "m1"),
    ])
    assert "pembuka" in json.loads(run(stop(path)))["systemMessage"]


def test_stop_string_content():
    path = transcript([("assistant", "**Jawaban:** port 9200 tertutup.", None)])
    assert "huruf tebal" in json.loads(run(stop(path)))["systemMessage"]


def test_stop_code_block_ignored():
    text = CLEAN_REPLY + "\n\n```bash\n# komentar\n- bukan butir — aja\nkirimlog kirim --config kirimlog.toml\n```"
    path = transcript([("assistant", [{"type": "text", "text": text}], "m1")])
    assert run(stop(path)) == ""


def _stop_message(text):
    path = transcript([("assistant", [{"type": "text", "text": text}], "m1")])
    out = run(stop(path))
    return json.loads(out)["systemMessage"] if out else ""


def test_stop_istilah_tegak_listed():
    message = _stop_message("Hasil output perintah itu sudah benar. Lalu, push perubahan itu.")
    assert message.startswith("bahasa-sederhana cek balasan: kata Inggris belum miring: output, push."), message
    assert "huruf miring" in message, message
    assert "Jawab dalam bentuk prosa." not in message, message


def test_stop_istilah_miring_silent():
    text = "Hasil *output* perintah itu sudah benar. Lalu, _push_ perubahan itu ke `main`."
    assert _stop_message(text) == ""


def test_stop_istilah_distinct_max_five():
    text = (
        "Simpan script dan Script itu. Lalu, push, commit, deploy, build, dan merge kode itu. "
        "Jalankan script lagi."
    )
    message = _stop_message(text)
    assert "kata Inggris belum miring: script, push, commit, deploy, build, dan 1 lainnya." in message, message
    assert message.count("script") == 1, message


def test_stop_istilah_code_quote_url_ignored():
    text = (
        "Jalankan `git push` lalu baca \"output\" di https://example.com/push/output. "
        "Kode ada di GitHub dan di src/hooks/lint_hook.py."
    )
    assert _stop_message(text) == ""


def test_stop_padanan_janggal_listed():
    message = _stop_message("Jalankan skrip itu, lalu baca keluaran dan keluaran lain.")
    assert message.startswith("bahasa-sederhana cek balasan: padanan janggal: skrip, keluaran."), message
    assert "Pakai istilah Inggris" in message, message


def test_stop_mixed_findings_order():
    text = "Tentu! Jalankan skrip itu dan lihat **output** di server."
    message = _stop_message(text)
    assert message.startswith("bahasa-sederhana cek balasan: 1 huruf tebal, 1 pembuka basa-basi. "), message
    assert ". Kata Inggris belum miring: output, server. Padanan janggal: skrip. " in message, message
    assert message.endswith(". Jawab dalam bentuk prosa."), message


def test_post_istilah_and_janggal_reported():
    path = write("istilah.md", "# Catatan kirimlog\n\nAlat kirimlog membaca skrip lalu menulis output.\n")
    reason = blocked(run(post(path)))
    assert "baris 3, istilah_tegak: output" in reason, reason
    assert "baris 3, padanan_janggal: skrip" in reason, reason


def test_post_istilah_miring_silent():
    path = write("istilah-miring.md", "# Catatan kirimlog\n\nAlat kirimlog membaca *script* lalu menulis _output_.\n")
    assert run(post(path)) == ""


def test_stop_missing_transcript_silent():
    assert run(stop(os.path.join(TMP, "tidak-ada.jsonl"))) == ""


def test_stop_broken_transcript_lines():
    path = os.path.join(TMP, "rusak.jsonl")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("bukan json\n[1, 2]\n")
        fh.write(json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": DIRTY_REPLY}]}}) + "\n")
        fh.write("{rusak\n")
    assert "systemMessage" in json.loads(run(stop(path)))


# ---------------------------------------------------------------------------
# Masukan yang salah


def test_bad_stdin_silent():
    assert run(None, raw="ini bukan json") == ""
    assert run(None, raw="") == ""
    assert run(None, raw="[1, 2, 3]") == ""
    assert run(None, raw='{"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": null}') == ""
    assert run(None, raw='{"hook_event_name": "Stop", "transcript_path": 42}') == ""


def test_unknown_event_silent():
    assert run({"hook_event_name": "SessionStart"}) == ""
    assert run({}) == ""


def main():
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_") and callable(fn)]
    failed = 0
    try:
        for name, fn in tests:
            try:
                fn()
            except Exception:  # noqa: BLE001
                failed += 1
                print("GAGAL %s" % name)
                traceback.print_exc()
            else:
                print("ok %s" % name)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    print("%d uji, %d gagal" % (len(tests), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
