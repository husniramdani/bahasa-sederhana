#!/usr/bin/env python3
"""Linter pola teks untuk Bahasa Sederhana.

Linter ini menghitung 14 jenis pelanggaran yang dapat ditangkap dengan pola
teks. Linter ini membaca pola, bukan tata bahasa. Pakai hasilnya untuk
membandingkan dua teks, bukan sebagai bukti kepatuhan.

Pemakaian:

    python3 evals/bahasa_lint.py --type procedural dokumen.md
    python3 evals/bahasa_lint.py --type reply - < balasan.txt
    python3 evals/bahasa_lint.py --type descriptive --gate 0 README.md
    python3 evals/bahasa_lint.py --self-test

Fungsi untuk modul lain:

    lint(text, text_type)         -> ringkasan dan jumlah per kategori
    lint_detail(text, text_type)  -> daftar {category, text, line}
    reader_check(text)            -> hitungan format yang terlihat di balasan obrolan

Cara menghitung:

- Frontmatter YAML, blok kode berpagar, tag HTML, dan komentar HTML dilewati.
- Kode sebaris, URL, dan teks di dalam tanda petik ganda dihitung satu kata
  (aturan BS8.5). Isi tanda petik tidak diperiksa, jadi berkas aturan dapat
  mengutip kata yang dilarang.
- Panjang kalimat juga menghitung teks dalam kurung sebagai satu kata (BS8.5).
  Nilai `words` menghitung semua kata, termasuk isi kurung.
- Setiap sel tabel, butir daftar, dan judul dihitung sebagai satu satuan
  kalimat tersendiri.
- Nomor baris selalu merujuk ke teks asli.

Hanya pustaka standar Python 3.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

TYPES = ("procedural", "descriptive", "reply")
LIMITS = {"procedural": 20, "descriptive": 25, "reply": None}

CATEGORIES = (
    "kalimat_terlalu_panjang",
    "kata_cakapan",
    "modal_terlarang",
    "pasif_bertumpuk",
    "anak_kalimat_lepas",
    "titik_koma",
    "tanda_pisah",
    "singkatan_latin",
    "kata_gaya_ai",
    "kata_tidak_baku",
    "terjemahan_harfiah",
    "pleonasme",
    "syarat_di_belakang",
    "rotasi_sinonim",
)

READER_KEYS = (
    "tanda_pisah",
    "huruf_tebal",
    "subjudul",
    "butir",
    "kata_cakapan",
    "pembuka",
    "penutup",
)

# Token pengganti. Setiap token dihitung satu kata dan tidak cocok dengan pola apa pun.
CODE = ""
URL = ""
QUOTE = ""
PAREN = ""
TOKEN_SHOW = {CODE: "`kode`", URL: "<url>", QUOTE: '"..."', PAREN: "(...)"}

WORD_RE = re.compile(r"[-]|\w+(?:[-.,/:'’+]\w+)*")

# Batas kata: huruf, angka, atau tanda hubung di sebelahnya berarti bukan kata utuh.
L = r"(?<![\w-])"
R = r"(?![\w-])"


def _flags_ci(pattern):
    return re.compile(pattern, re.IGNORECASE)


# ---------------------------------------------------------------------------
# Daftar kata dari berkas TSV

def _load_first_column(name):
    path = os.path.join(HERE, name)
    words = []
    try:
        with open(path, encoding="utf-8") as fh:
            for raw in fh:
                line = raw.rstrip("\n")
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                first = line.split("\t", 1)[0].strip()
                if first:
                    words.append(first)
    except OSError:
        pass
    return words


def _phrase_regex(phrases):
    if not phrases:
        return None
    parts = []
    for phrase in sorted(set(phrases), key=len, reverse=True):
        parts.append(r"\s+".join(re.escape(w) for w in phrase.split()))
    return _flags_ci(L + "(?:" + "|".join(parts) + ")" + R)


SLOP_RE = _phrase_regex(_load_first_column("slop.tsv"))
NONBAKU_RE = _phrase_regex(_load_first_column("nonbaku.tsv"))
ANDA_LOWER_RE = re.compile(L + "anda" + R)

# ---------------------------------------------------------------------------
# Pola per kategori

CAKAPAN_WORDS = (
    "yg dgn utk tdk krn sdh blm tsb jg tp bgt gk "
    "gak nggak ngga enggak udah aja banget bikin pake kalo gimana sih dong deh "
    "nih kok emang gitu kayak"
).split()
CAKAPAN_RE = _flags_ci(
    L + "(?:" + "|".join(CAKAPAN_WORDS) + ")" + R + "|" + L + r"dr(?![\w.-])"
)

MODAL_RE = _flags_ci(
    L + r"(?:sebaiknya|seharusnya|hendaknya|mungkin|barangkali|bisa\s+jadi)" + R
)
# Kata ber-se- yang bukan adjektiva. "sesuatu mungkin" tetap pelanggaran.
SE_NOT_ADJ = set(
    "sesuatu seseorang semua setiap sering selalu sedang sekarang sebuah seorang "
    "sesudah sebelum setelah selama sementara seperti sehingga serta segera sendiri "
    "sekali sebagai secara sesuai".split()
)

PASIF_RE = _flags_ci(L + r"(telah|sudah)\s+(di(?:-\w+|[a-z]\w+))" + R)
OLEH_RE = _flags_ci(L + "oleh" + R)

AKL_RE = _flags_ci(
    r",\s*(?:sehingga|yang)\s+(?:memudahkan|menjadikan\w*|memungkinkan|membuat|menyebabkan)"
    + R
)
# Kata kerja tanpa subjek langsung setelah koma. Jika kata itu diikuti koma,
# "dan", atau "atau", kata itu bagian dari daftar kata kerja dengan subjek yang sama.
AKL_BARE_RE = _flags_ci(
    r",\s*(?:memudahkan|menjadikannya|memungkinkan)" + R + r"(?![ \t]*,|\s+(?:dan|atau)" + R + ")"
)

DASH_EM_RE = re.compile(r"(?<=\S)[ \t]*—[ \t]*(?=\S)")
DASH_EN_RE = re.compile(r"(?<=\S)[ \t]+–[ \t]+(?=\S)")
DASH_HYPHEN_RE = re.compile(r"(?<=\S)[ \t]+-[ \t]+(?=\S)")
DASH_DOUBLE_RE = re.compile(r"(?<=\S)[ \t]+--[ \t]+(?=\S)|(?<=[^\W\d_])--(?=[^\W\d_])")

LATIN_RE = _flags_ci(r"(?<![\w.])(?:dll|dsb|dst|etc)(?!\w)\.?|(?<![\w.])(?:e\.g|i\.e)(?!\w)\.?")

TH_MANA_RE = _flags_ci(L + r"(?:di|yang)\s+mana" + R + r"(?!\s+(?:pun|saja)" + R + ")")
TH_RANGKA_RE = _flags_ci(L + r"dalam\s+rangka" + R)
TH_LAKUKAN_RE = _flags_ci(
    L
    + r"(?:melakukan|lakukan|lakukanlah|dilakukan)\s+"
    + r"(?:pe[a-z]{2,}an(?:nya)?|instalasi|konfigurasi|verifikasi|validasi|update|deploy|restart|backup)"
    + R
)
TH_FRASA_RE = _flags_ci(
    L + r"(?:mengambil\s+tempat|memberikan\s+dukungan|membuat\s+perubahan)" + R
)

PLEONASME_RES = [
    _flags_ci(L + p + R)
    for p in (
        r"adalah\s+merupakan",
        r"agar\s+supaya",
        r"demi\s+untuk",
        r"sangat\s+\w+\s+sekali",
        r"para\s+(\w+)-\1",
        r"naik\s+ke\s+atas",
        r"turun\s+ke\s+bawah",
        r"mundur\s+ke\s+belakang",
        r"maju\s+ke\s+depan",
    )
]

COND_WORDS = ("jika", "apabila", "bila", "kalau")
COND_INNER_RE = _flags_ci(r"\s(?:jika|apabila|bila|kalau)" + R)
COND_LEAD_RE = _flags_ci(r"^\W*(?:\w+\s+){0,2}?\w+,\s*(?:jika|apabila|bila|kalau)" + R)

SYNONYM_SETS = (
    ("periksa", (
        ("periksa", r"(?:di|ter)?periksa(?:kan|lah|nya)?|(?:me|pe)meriksa(?:an|kan|nya|annya)?"),
        ("cek", r"(?:di|ter|nge|menge|penge|me|pe)?-?cek(?:an|nya|lah|kan|annya)?"),
        ("verifikasi", r"(?:di|mem|me|ter|pem)?-?verifikasi(?:kan|nya|lah)?"),
        ("konfirmasi", r"(?:di|ter|meng|me)?-?konfirmasi(?:kan|nya|lah)?|mengonfirmasi(?:kan|nya)?"),
    )),
    ("konfigurasi", (
        ("konfigurasi", r"(?:di|ter|meng|pe|peng)?-?konfigurasi(?:kan|nya|lah)?|mengonfigurasi(?:kan|nya)?"),
        ("config", r"(?:di|nge|meng)?-?config(?:s|nya|-nya)?"),
    )),
    ("pengaturan", (
        ("pengaturan", r"pengaturan(?:nya)?"),
        ("setelan", r"setelan(?:nya)?"),
        ("settings", r"settings?(?:-?nya)?"),
    )),
    ("jika", (
        ("jika", r"jika"),
        ("apabila", r"apabila"),
        ("bila", r"bila"),
        ("kalau", r"kalau"),
        ("seandainya", r"seandainya"),
    )),
    ("sapaan", (
        ("anda", r"anda(?:lah)?"),
        ("kamu", r"kamu(?:lah)?"),
    )),
    ("kesalahan", (
        ("kesalahan", r"kesalahan(?:nya)?"),
        ("error", r"errors?(?:-?nya)?"),
        ("galat", r"galat(?:nya)?"),
    )),
)
_SYN_COMPILED = [
    (set_name, [(stem, re.compile(pat)) for stem, pat in stems]) for set_name, stems in SYNONYM_SETS
]

# Singkatan gelar dan sejenisnya. Titik setelah kata ini tidak mengakhiri kalimat.
NO_SPLIT_ABBREV = set("dr prof ir drs dra no hlm mis bpk sdr jl tn ny vs st".split())

OPENER_RE = _flags_ci(
    r"^(?:tentu|pertanyaan\s+bagus|berikut\s+adalah|dengan\s+senang\s+hati|sure|great\s+question|certainly)"
    + R
    + r"|^(?:baik|siap|oke|ok)\s*[,!.]"
)
CLOSER_RE = _flags_ci(
    r"semoga\s+(?:membantu|bermanfaat)|jangan\s+ragu\s+untuk|jika\s+ada\s+pertanyaan"
    r"|beri\s+tahu\s+saya\s+jika|hope\s+this\s+helps|let\s+me\s+know\s+if"
)
BOLD_RE = re.compile(r"\*\*(?=\S)[^\n]+?(?<=\S)\*\*|(?<!\w)__(?=\S)[^\n]+?(?<=\S)__(?!\w)")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S")
BULLET_RE = re.compile(r"^\s*(?:>\s*)*(?:[-*+•]|\d{1,3}[.)])\s+\S")

# ---------------------------------------------------------------------------
# Praproses


def _normalize(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.startswith("﻿"):
        text = text[1:]
    return text


def _strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return [""] * (i + 1) + lines[i + 1:]
    return lines


FENCE_RE = re.compile(r"^\s*(?:>\s*)*(`{3,}|~{3,})(.*)$")


def _mask_fences(lines):
    out = []
    fence = None
    for line in lines:
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                out.append("")
            else:
                out.append(line)
        else:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
            out.append("")
    return out


INLINE_CODE_RE = re.compile(r"(`+)(?!`)([^\n]*?[^`\n])\1(?!`)")
URL_RE = re.compile(r"(?:https?://|www\.)[^\s<>\"'`“”]+")
MD_LINK_RE = re.compile(r"!?\[([^\]\n]*)\]\([^)\n]*\)")
MD_REFLINK_RE = re.compile(r"\[([^\]\n]*)\]\[[^\]\n]*\]")
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HTML_TAG_RE = re.compile(r"</?[A-Za-z][\w-]*(?:\s[^<>]*)?/?>")
HTML_ENTITY_RE = re.compile(r"&#?\w+;")
QUOTE_RE = re.compile(r"\"[^\"\n]+\"|“[^”\n]+”")


def _url_sub(match):
    url = match.group(0)
    trail = ""
    while url:
        last = url[-1]
        if last in ".,;:!?'":
            pass
        elif last == ")" and url.count("(") < url.count(")"):
            pass
        elif last == "]" and url.count("[") < url.count("]"):
            pass
        else:
            break
        trail = last + trail
        url = url[:-1]
    return URL + trail


def _keep_newlines(match):
    return "\n" * match.group(0).count("\n")


def preprocess(text):
    """Kembalikan teks bertopeng dengan jumlah baris yang sama dengan teks asli."""
    lines = _normalize(text).split("\n")
    lines = _strip_frontmatter(lines)
    lines = _mask_fences(lines)
    masked = "\n".join(lines)
    masked = HTML_COMMENT_RE.sub(_keep_newlines, masked)
    masked = INLINE_CODE_RE.sub(CODE, masked)
    masked = URL_RE.sub(_url_sub, masked)
    masked = MD_LINK_RE.sub(r"\1", masked)
    masked = MD_REFLINK_RE.sub(r"\1", masked)
    masked = masked.replace("<" + URL + ">", URL)
    masked = HTML_TAG_RE.sub(" ", masked)
    masked = HTML_ENTITY_RE.sub(" ", masked)
    masked = QUOTE_RE.sub(QUOTE, masked)
    return masked


# ---------------------------------------------------------------------------
# Satuan kalimat

HR_RE = re.compile(r"^(?:[-*_=][ \t]*){3,}$")
TABLE_SEP_RE = re.compile(r"^\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?$")
HEADING_LINE_RE = re.compile(r"^#{1,6}[ \t]+(.*?)[ \t#]*$")
LIST_RE = re.compile(r"^(?:[-*+•]|\d{1,3}[.)])[ \t]+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^[ \t]*(?:>[ \t]?)+")


def _clean_emphasis(segment):
    segment = segment.replace("**", "").replace("~~", "").replace("*", "")
    segment = re.sub(r"(?<!\w)_+(?=\w)|(?<=\w)_+(?!\w)", "", segment)
    return segment


def _units(masked):
    """Bagi teks bertopeng menjadi satuan: paragraf, butir daftar, sel tabel, atau judul.

    Setiap satuan adalah (teks, daftar_nomor_baris). Baris ke-k dalam teks satuan
    berasal dari daftar_nomor_baris[k].
    """
    units = []
    current = []

    def flush():
        if current:
            units.append(("\n".join(seg for _, seg in current), [n for n, _ in current]))
            current.clear()

    for number, raw in enumerate(masked.split("\n"), 1):
        line = BLOCKQUOTE_RE.sub("", raw)
        stripped = line.strip()
        if not stripped or HR_RE.match(stripped):
            flush()
            continue
        if stripped.startswith("|"):
            flush()
            if TABLE_SEP_RE.match(stripped):
                continue
            body = stripped[1:]
            if body.endswith("|"):
                body = body[:-1]
            for cell in body.split("|"):
                cell = _clean_emphasis(cell).strip()
                if cell:
                    units.append((cell, [number]))
            continue
        heading = HEADING_LINE_RE.match(stripped)
        if heading:
            flush()
            text = _clean_emphasis(heading.group(1)).strip()
            if text:
                units.append((text, [number]))
            continue
        item = LIST_RE.match(stripped)
        if item:
            flush()
            current.append((number, _clean_emphasis(item.group(1)).strip()))
            continue
        current.append((number, _clean_emphasis(stripped)))
    flush()
    return units


SENT_END_RE = re.compile(r"([.!?…]+)([\"'”’)\]]*)(\s+|$)")


def _split_sentences(text):
    """Kembalikan daftar (teks_kalimat, posisi_awal)."""
    out = []
    start = 0
    for m in SENT_END_RE.finditer(text):
        end = m.end(2)
        if m.end() < len(text):
            nxt = text[m.end()]
            if nxt.isalpha() and nxt.islower():
                continue
            before = re.search(r"(\w+)$", text[start:m.start(1)])
            if m.group(1) == "." and before and before.group(1).lower() in NO_SPLIT_ABBREV:
                continue
        piece = text[start:end]
        if piece.strip():
            lead = len(piece) - len(piece.lstrip())
            out.append((piece.strip(), start + lead))
        start = m.end()
    piece = text[start:]
    if piece.strip():
        lead = len(piece) - len(piece.lstrip())
        out.append((piece.strip(), start + lead))
    return out


def _count_words(text):
    return len(WORD_RE.findall(text))


def _length_words(sentence):
    """Panjang kalimat menurut BS8.5: teks dalam kurung dihitung satu kata."""
    collapsed = sentence
    for _ in range(3):
        collapsed = re.sub(r"\([^()]*\)", " " + PAREN + " ", collapsed)
    return _count_words(collapsed)


def _context(sentence, start, end, pad=20):
    """Potong konteks di sekitar temuan pada batas kata."""
    a = max(0, start - pad)
    b = min(len(sentence), end + pad)
    if a > 0:
        space = sentence.find(" ", a, start)
        a = space + 1 if space != -1 else a
    if b < len(sentence):
        space = sentence.rfind(" ", end, b)
        b = space if space != -1 else b
    return sentence[a:b]


def _show(text, limit=80):
    for token, shown in TOKEN_SHOW.items():
        text = text.replace(token, shown)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[: limit - 3].rstrip() + "..."
    return text


# ---------------------------------------------------------------------------
# Pemeriksaan per kalimat


def _dash_hits(sentence):
    hits = []
    for regex, need_check_digits in (
        (DASH_EM_RE, True),
        (DASH_EN_RE, True),
        (DASH_HYPHEN_RE, True),
        (DASH_DOUBLE_RE, False),
    ):
        for m in regex.finditer(sentence):
            left = sentence[m.start() - 1] if m.start() > 0 else ""
            right = sentence[m.end()] if m.end() < len(sentence) else ""
            if need_check_digits and left.isdigit() and right.isdigit():
                continue
            hits.append((m.start(), _context(sentence, m.start(), m.end(), 15)))
    return hits


def _modal_hits(sentence):
    hits = []
    for m in MODAL_RE.finditer(sentence):
        word = m.group(0).lower()
        if word == "mungkin":
            prev = re.search(r"(\w+)\s+$", sentence[: m.start()])
            if prev:
                p = prev.group(1).lower()
                if p.startswith("se") and len(p) > 4 and p not in SE_NOT_ADJ:
                    continue
        hits.append((m.start(), m.group(0)))
    return hits


def _pasif_hits(sentence):
    hits = []
    for m in PASIF_RE.finditer(sentence):
        aux = m.group(1).lower()
        verb = m.group(2).lower()
        if (aux == "telah" and verb == "dilakukan") or OLEH_RE.search(sentence, m.end()):
            hits.append((m.start(), sentence[m.start(): m.end() + 30]))
    return hits


def _syarat_hit(sentence):
    if re.search(r"\?\s*$", sentence):
        return None
    words = WORD_RE.findall(sentence)
    if not words or words[0].lower() in COND_WORDS:
        return None
    if COND_LEAD_RE.match(sentence):
        return None
    first = WORD_RE.search(sentence)
    m = COND_INNER_RE.search(sentence, first.end() if first else 0)
    if m:
        return (m.start() + 1, sentence)
    return None


def _synonym_tokens(sentence):
    for m in WORD_RE.finditer(sentence):
        word = m.group(0).lower()
        if m.start() > 0 and sentence[m.start() - 1] == "-":
            continue  # flag CLI seperti --config
        for set_name, stems in _SYN_COMPILED:
            for stem, regex in stems:
                if regex.fullmatch(word):
                    yield m.start(), set_name, stem, m.group(0)
                    break


def lint_detail(text, text_type):
    """Kembalikan daftar temuan {category, text, line}, urut menurut baris."""
    if text_type not in TYPES:
        raise ValueError("jenis teks tidak dikenal: %r" % (text_type,))
    details, _ = _analyze(text, text_type)
    return details


def _analyze(text, text_type):
    limit = LIMITS[text_type]
    masked = preprocess(text)
    details = []
    stats = {"words": 0, "lengths": []}
    first_stem = {}
    seen_extra = set()

    for unit_text, line_numbers in _units(masked):
        def line_of(offset, _t=unit_text, _n=line_numbers):
            return _n[min(_t.count("\n", 0, offset), len(_n) - 1)]

        for sentence, s_off in _split_sentences(unit_text):
            words = _count_words(sentence)
            if words == 0:
                continue
            stats["words"] += words
            length = _length_words(sentence)
            stats["lengths"].append(length)

            def add(category, offset, snippet, _s_off=s_off):
                details.append({
                    "category": category,
                    "text": _show(snippet),
                    "line": line_of(_s_off + offset),
                })

            if limit is not None and length > limit:
                add("kalimat_terlalu_panjang", 0, "%s (%d kata)" % (_show(sentence, 60), length))
            for m in CAKAPAN_RE.finditer(sentence):
                add("kata_cakapan", m.start(), m.group(0))
            for off, snip in _modal_hits(sentence):
                add("modal_terlarang", off, snip)
            for off, snip in _pasif_hits(sentence):
                add("pasif_bertumpuk", off, snip)
            for regex in (AKL_RE, AKL_BARE_RE):
                for m in regex.finditer(sentence):
                    add("anak_kalimat_lepas", m.start(), m.group(0).lstrip(", "))
            for m in re.finditer(";", sentence):
                add("titik_koma", m.start(), _context(sentence, m.start(), m.end()))
            for off, snip in _dash_hits(sentence):
                add("tanda_pisah", off, snip)
            for m in LATIN_RE.finditer(sentence):
                add("singkatan_latin", m.start(), m.group(0))
            if SLOP_RE is not None:
                for m in SLOP_RE.finditer(sentence):
                    add("kata_gaya_ai", m.start(), m.group(0))
            if NONBAKU_RE is not None:
                for m in NONBAKU_RE.finditer(sentence):
                    add("kata_tidak_baku", m.start(), m.group(0))
            for m in ANDA_LOWER_RE.finditer(sentence):
                add("kata_tidak_baku", m.start(), m.group(0))
            if not re.search(r"\?\s*$", sentence):
                for m in TH_MANA_RE.finditer(sentence):
                    add("terjemahan_harfiah", m.start(), m.group(0))
            for regex in (TH_RANGKA_RE, TH_LAKUKAN_RE, TH_FRASA_RE):
                for m in regex.finditer(sentence):
                    add("terjemahan_harfiah", m.start(), m.group(0))
            for regex in PLEONASME_RES:
                for m in regex.finditer(sentence):
                    add("pleonasme", m.start(), m.group(0))
            if text_type == "procedural":
                hit = _syarat_hit(sentence)
                if hit:
                    add("syarat_di_belakang", hit[0], _show(hit[1], 70))
            for off, set_name, stem, word in _synonym_tokens(sentence):
                if set_name not in first_stem:
                    first_stem[set_name] = stem
                elif stem != first_stem[set_name] and (set_name, stem) not in seen_extra:
                    seen_extra.add((set_name, stem))
                    add("rotasi_sinonim", off, "%s (sudah memakai %s)" % (word, first_stem[set_name]))

    details.sort(key=lambda d: d["line"])
    return details, stats


def lint(text, text_type):
    """Kembalikan ringkasan pelanggaran untuk satu teks."""
    if text_type not in TYPES:
        raise ValueError("jenis teks tidak dikenal: %r" % (text_type,))
    details, stats = _analyze(text, text_type)
    counts = {c: 0 for c in CATEGORIES}
    for d in details:
        counts[d["category"]] += 1
    lengths = stats["lengths"]
    words = stats["words"]
    total = sum(counts.values())
    return {
        "type": text_type,
        "words": words,
        "sentences": len(lengths),
        "mean_sentence_words": round(sum(lengths) / len(lengths), 1) if lengths else 0.0,
        "longest_sentence_words": max(lengths) if lengths else 0,
        "violations": counts,
        "violations_total": total,
        "violations_per_100w": round(total * 100.0 / words, 2) if words else 0.0,
    }


# ---------------------------------------------------------------------------
# Pemeriksaan balasan obrolan


def reader_check(text):
    """Hitung format dan basa-basi yang terlihat pembaca di balasan obrolan."""
    lines = _mask_fences(_normalize(text).split("\n"))
    prose = INLINE_CODE_RE.sub(CODE, "\n".join(lines))
    details = lint_detail(text, "reply")

    counts = {k: 0 for k in READER_KEYS}
    counts["tanda_pisah"] = sum(1 for d in details if d["category"] == "tanda_pisah")
    counts["kata_cakapan"] = sum(1 for d in details if d["category"] == "kata_cakapan")
    counts["huruf_tebal"] = len(BOLD_RE.findall(prose))
    for line in prose.split("\n"):
        if HEADING_RE.match(line):
            counts["subjudul"] += 1
        elif BULLET_RE.match(line):
            counts["butir"] += 1

    first = ""
    for line in prose.split("\n"):
        if line.strip():
            first = line
            break
    first = re.sub(r"^[\s#>*_\-]+", "", first)
    counts["pembuka"] = 1 if OPENER_RE.search(first) else 0

    tail = prose.strip()[-300:]
    counts["penutup"] = 1 if CLOSER_RE.search(tail) else 0

    counts["visible_total"] = sum(counts[k] for k in READER_KEYS)
    return counts


# ---------------------------------------------------------------------------
# Uji bawaan

SLOPPY_FIXTURE = """---
judul: Panduan kirimlog
---

# Memulai kirimlog

kirimlog adalah merupakan tool yg dirancang untuk mengirim log ke OpenSearch secara mulus, sehingga memudahkan tim memantau aplikasi.

Sebelum mulai, kamu sebaiknya cek dulu apakah Python sudah terpasang di mesin anda, karena tanpa Python kirimlog gak bisa dipasang dan proses pemasangan akan gagal di tengah jalan.

1. Lakukan instalasi dengan `pip install kirimlog`; tunggu sampai selesai.
2. Buka config `kirimlog.toml` — isi alamat OpenSearch, port 9200, nama indeks, dll.
3. Jalankan `kirimlog kirim --config kirimlog.toml` apabila konfigurasi sudah benar.
4. Konfigurasi itu telah diperiksa oleh tim sebelum rilis.

Jika muncul error 401, verifikasi kata sandi di server di mana pengguna OpenSearch dibuat.
"""

CLEAN_FIXTURE = """# Memulai kirimlog

Alat kirimlog membaca berkas log aplikasi dan mengirim isinya ke OpenSearch.

## Pasang kirimlog

1. Pasang kirimlog dengan `pip install kirimlog`.
2. Buka berkas konfigurasi `kirimlog.toml`.
3. Isi alamat OpenSearch dan port 9200.
4. Jalankan `kirimlog kirim --config kirimlog.toml`.

## Jika pengiriman gagal

Jika kirimlog menampilkan `connection refused`, pastikan OpenSearch berjalan di port 9200.

Jika OpenSearch menjawab dengan HTTP 401, periksa kata sandi di `kirimlog.toml`.

Jika OpenSearch menjawab dengan HTTP 403, beri pengguna itu izin menulis ke indeks. Panduan izin ada di https://example.com/kirimlog/izin.
"""


def _self_test():
    checks = []

    def check(name, condition, info=""):
        checks.append(name)
        if not condition:
            raise AssertionError("%s gagal %s" % (name, info))

    def count(text, text_type, category):
        return lint(text, text_type)["violations"][category]

    # Daftar kata dari TSV harus termuat.
    check("tsv_termuat", SLOP_RE is not None and NONBAKU_RE is not None)

    # Fixture berantakan memicu setiap kategori.
    sloppy = lint(SLOPPY_FIXTURE, "procedural")
    for category in CATEGORIES:
        check("berantakan_" + category, sloppy["violations"][category] >= 1, json.dumps(sloppy["violations"]))
    check("kunci_lengkap", set(sloppy["violations"]) == set(CATEGORIES))
    check("total_sama", sloppy["violations_total"] == sum(sloppy["violations"].values()))
    for key in ("type", "words", "sentences", "mean_sentence_words", "longest_sentence_words",
                "violations", "violations_total", "violations_per_100w"):
        check("kunci_" + key, key in sloppy)

    # Fixture bersih tidak punya pelanggaran.
    for text_type in ("procedural", "descriptive"):
        clean = lint(CLEAN_FIXTURE, text_type)
        check("bersih_" + text_type, clean["violations_total"] == 0, json.dumps(lint_detail(CLEAN_FIXTURE, text_type)))

    # Jumlah detail sama dengan jumlah ringkasan.
    for fixture in (SLOPPY_FIXTURE, CLEAN_FIXTURE):
        for text_type in TYPES:
            summary = lint(fixture, text_type)["violations"]
            detail = {c: 0 for c in CATEGORIES}
            for d in lint_detail(fixture, text_type):
                detail[d["category"]] += 1
                check("detail_baris_int", isinstance(d["line"], int) and d["line"] >= 1)
            check("detail_sama_" + text_type, detail == summary)

    # "di mana" dalam pertanyaan dan "di mana pun" bukan pelanggaran.
    check("di_mana_tanya", count("Di mana kirimlog menyimpan antrean batch?", "descriptive", "terjemahan_harfiah") == 0)
    check("di_mana_pun", count("Jalankan kirimlog di mana pun Python tersedia.", "procedural", "terjemahan_harfiah") == 0)
    check("di_mana_saja", count("Pengirim dapat berjalan di mana saja.", "descriptive", "terjemahan_harfiah") == 0)
    check("di_mana_penghubung", count("Server di mana kirimlog berjalan memakai Python 3.", "descriptive", "terjemahan_harfiah") == 1)

    # "se-ADJ mungkin" bukan modalitas.
    check("sesingkat_mungkin", count("Tulis langkah ini sesingkat mungkin.", "procedural", "modal_terlarang") == 0)
    check("secepat_mungkin", count("Ganti sertifikat itu secepat mungkin.", "procedural", "modal_terlarang") == 0)
    check("mungkin_dilarang", count("Pengiriman mungkin gagal.", "descriptive", "modal_terlarang") == 1)

    # Bentuk baku yang mirip bentuk tidak baku.
    for word, sentence in (
        ("mengkritik", "Tim keamanan mengkritik rancangan pengirim yang lama."),
        ("memproses", "Pengurai memproses setiap baris log."),
        ("dikirim", "Setiap batch dikirim ke OpenSearch dengan bulk API."),
    ):
        check("baku_" + word, lint(sentence, "descriptive")["violations_total"] == 0, json.dumps(lint_detail(sentence, "descriptive")))

    # Rentang angka dan flag bukan tanda pisah.
    check("rentang_tahun", count("Versi lama dipakai pada 2010—2013.", "descriptive", "tanda_pisah") == 0)
    check("rentang_angka", count("Setiap batch berisi 5–10 MB data.", "descriptive", "tanda_pisah") == 0)
    check("flag_cli", count("Tambahkan flag --dry-run untuk uji coba.", "procedural", "tanda_pisah") == 0)
    check("pisah_em", count("Pengirim cepat — pengurai lambat.", "descriptive", "tanda_pisah") == 1)
    check("pisah_hubung_berspasi", count("Pengirim cepat - pengurai lambat.", "descriptive", "tanda_pisah") == 1)
    check("pisah_hubung_ganda", count("Pengirim cepat -- pengurai lambat.", "descriptive", "tanda_pisah") == 1)

    # Daftar kata kerja dengan subjek yang sama bukan anak kalimat lepas.
    check("daftar_kata_kerja", count("Kirimlog membaca, mengurai, dan mengirim log aplikasi.", "descriptive", "anak_kalimat_lepas") == 0)
    check("daftar_memungkinkan", count("Pengirim mengelompokkan, memungkinkan, dan mengirim batch.", "descriptive", "anak_kalimat_lepas") == 0)
    check("anak_kalimat_sehingga", count("Pengirim mengulang batch, sehingga memudahkan pemulihan.", "descriptive", "anak_kalimat_lepas") == 1)
    check("anak_kalimat_bare", count("Versi 3.0 menambah flag baru, memungkinkan uji coba.", "descriptive", "anak_kalimat_lepas") == 1)

    # Syarat di belakang hanya untuk prosedur.
    check("syarat_deskripsi", count("Penghapusan indeks lama aman hanya jika snapshot sudah dibuat.", "descriptive", "syarat_di_belakang") == 0)
    check("syarat_prosedur", count("Hapus indeks lama jika snapshot sudah dibuat.", "procedural", "syarat_di_belakang") == 1)
    check("syarat_penghubung", count("Lalu, jika snapshot sudah ada, hapus indeks lama.", "procedural", "syarat_di_belakang") == 0)
    check("syarat_di_depan", count("Jika snapshot sudah ada, hapus indeks lama.", "procedural", "syarat_di_belakang") == 0)

    # Kata terlarang di dalam tanda petik tidak dihitung.
    quoted = 'Jangan tulis "sebaiknya" atau “mungkin” di runbook kirimlog.'
    check("kutipan", lint(quoted, "procedural")["violations_total"] == 0, json.dumps(lint_detail(quoted, "procedural")))
    check("kutipan_satu_kata", lint('Tulis "jalankan kirimlog dengan konfigurasi baru".', "procedural")["words"] == 2)

    # Nomor baris tetap benar setelah frontmatter, tabel, dan blok kode.
    table_text = (
        "---\njudul: x\n---\n"
        "| Kolom | Arti |\n|---|---|\n| `source_host` | Nama host sumber |\n"
        "\n```toml\nsource_host = \"app-1\" ; komentar\n```\n\n"
        "Jalankan kirimlog; tunggu sampai selesai.\n"
    )
    hits = lint_detail(table_text, "procedural")
    check("baris_setelah_tabel", [(d["category"], d["line"]) for d in hits] == [("titik_koma", 12)], json.dumps(hits))
    check("sel_tabel_kalimat", lint(table_text, "procedural")["sentences"] == 5)

    # URL dalam kurung yang diikuti titik.
    url_text = "Baca panduan OpenSearch (https://opensearch.org/docs/latest). Lalu, jalankan kirimlog."
    url_lint = lint(url_text, "procedural")
    check("url_kurung_kalimat", url_lint["sentences"] == 2, json.dumps(url_lint))
    check("url_kurung_bersih", url_lint["violations_total"] == 0)
    check("url_satu_kata", lint("Buka https://example.com/a-b--c;d sekarang.", "procedural")["words"] == 3)
    check("tautan_markdown", lint("Baca [panduan izin](https://example.com/izin). Lalu, kirim ulang batch.", "procedural")["sentences"] == 2)

    # Kode sebaris dihitung satu kata. Blok kode diabaikan.
    check("kode_satu_kata", lint("Jalankan `kirimlog kirim --config kirimlog.toml` sekarang.", "procedural")["words"] == 3)
    check("blok_kode_diabaikan", lint("```\nsebaiknya; yg -- dll\n```\nJalankan kirimlog.", "procedural")["violations_total"] == 0)

    # Tag HTML diabaikan.
    check("tag_html", lint('<p align="center">Alat kirimlog mengirim log.</p>', "descriptive")["violations_total"] == 0)

    # "dr." sebagai gelar bukan singkatan obrolan.
    check("gelar_dr", count("Rancangan ini ditinjau oleh dr. Sari.", "descriptive", "kata_cakapan") == 0)
    check("singkatan_dr", count("Ambil log dr server lama.", "procedural", "kata_cakapan") == 1)

    # "anda" kecil melanggar, "Anda" tidak.
    check("anda_kecil", count("Pasang kirimlog di laptop anda.", "procedural", "kata_tidak_baku") == 1)
    check("anda_kapital", count("Pasang kirimlog di laptop Anda.", "procedural", "kata_tidak_baku") == 0)

    # Batas kalimat per jenis teks.
    long21 = " ".join(["kata"] * 20) + " akhir."
    check("batas_prosedur", count(long21, "procedural", "kalimat_terlalu_panjang") == 1)
    check("batas_deskripsi", count(long21, "descriptive", "kalimat_terlalu_panjang") == 0)
    check("batas_balasan", count(" ".join(["kata"] * 80) + ".", "reply", "kalimat_terlalu_panjang") == 0)
    check("kurung_satu_kata", count(" ".join(["kata"] * 18) + " (satu dua tiga empat lima) akhir.", "procedural", "kalimat_terlalu_panjang") == 0)

    # Rotasi sinonim melapor setiap kata setelah kata pertama, sekali per kata.
    rot = lint("Periksa log. Cek port. Cek lagi. Lalu, verifikasi indeks.", "procedural")["violations"]["rotasi_sinonim"]
    check("rotasi_sekali_per_kata", rot == 2)
    check("rotasi_flag", count("Isi konfigurasi baru. Jalankan kirimlog dengan --config.", "procedural", "rotasi_sinonim") == 0)

    # Jenis teks yang tidak dikenal.
    try:
        lint("x", "lain")
        raised = False
    except ValueError:
        raised = True
    check("jenis_tidak_dikenal", raised)

    # Pemeriksaan balasan obrolan.
    messy = (
        "Tentu! Berikut penjelasannya.\n\n## Penyebab\n\n"
        "- **Port 9200** tertutup — OpenSearch belum jalan\n"
        "- Kata sandi salah, jadi muncul 401 aja\n\n"
        "Semoga membantu!"
    )
    rc = reader_check(messy)
    check("balasan_kunci", set(rc) == set(READER_KEYS) | {"visible_total"})
    check("balasan_pembuka", rc["pembuka"] == 1)
    check("balasan_penutup", rc["penutup"] == 1)
    check("balasan_subjudul", rc["subjudul"] == 1)
    check("balasan_butir", rc["butir"] == 2)
    check("balasan_tebal", rc["huruf_tebal"] == 1)
    check("balasan_pisah", rc["tanda_pisah"] == 1)
    check("balasan_cakapan", rc["kata_cakapan"] == 1)
    check("balasan_total", rc["visible_total"] == sum(rc[k] for k in READER_KEYS))
    calm = (
        "Port 9200 di host OpenSearch tertutup. Akibatnya, kirimlog berhenti dengan `connection refused`. "
        "Jalankan OpenSearch dulu, lalu kirim ulang batch itu.\n\n```bash\nkirimlog kirim --config kirimlog.toml\n- bukan butir\n```"
    )
    check("balasan_bersih", reader_check(calm)["visible_total"] == 0, json.dumps(reader_check(calm)))
    check("balasan_inggris", reader_check("Sure, here it is. Hope this helps!")["visible_total"] == 2)
    check("balasan_baik_biasa", reader_check("Baik versi lama maupun versi 3.0 membaca berkas yang sama.")["pembuka"] == 0)

    return len(checks)


# ---------------------------------------------------------------------------
# CLI


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Hitung pelanggaran Bahasa Sederhana yang dapat ditangkap dengan pola teks."
    )
    parser.add_argument("--type", choices=TYPES, help="jenis teks: procedural, descriptive, atau reply")
    parser.add_argument("--gate", type=int, default=None, help="keluar dengan kode 1 jika total pelanggaran lebih dari N")
    parser.add_argument("--detail", action="store_true", help="sertakan daftar temuan per baris")
    parser.add_argument("--self-test", action="store_true", help="jalankan uji bawaan")
    parser.add_argument("file", nargs="?", help="berkas yang diperiksa, atau - untuk stdin")
    args = parser.parse_args(argv)

    if args.self_test:
        try:
            n = _self_test()
        except AssertionError as exc:
            print("self-test GAGAL: %s" % exc)
            return 1
        print("self-test OK: %d pemeriksaan lulus" % n)
        return 0

    if not args.type or not args.file:
        parser.error("--type dan FILE wajib diisi, kecuali dengan --self-test")

    if args.file == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(args.file, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print("Berkas tidak dapat dibaca: %s" % exc, file=sys.stderr)
            return 2

    result = lint(text, args.type)
    if args.detail:
        result["detail"] = lint_detail(text, args.type)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.gate is not None and result["violations_total"] > args.gate:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
