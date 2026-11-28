"""Measure a LaTeX draft's prose against the theory or systems tone profile.

Usage: python3 tone_check.py <main.tex | paper_dir> [--profile theory|systems] [--section intro|related|method|experiments|conclusion]

Reads .tex files as text only; follows \\input/\\include; ignores the appendix.
Rates are per 1,000 words of prose (about one page of a two-column IEEE paper).
Rates on fewer than ~1,500 words are noisy; treat a single flag on a short excerpt as a hint, not a verdict.
"""
import argparse, re, statistics as st, sys
from pathlib import Path

# Bands blend per-paper quartiles: 2/3 hand-picked author papers + 1/3 ICRA 2024-26 finalists.
# One-sided ceilings sit near the blended 75th percentile and floors near the blended 25th;
# two-sided bands (sentence and paragraph length, punctuation caps) are wider. On the calibration
# corpus, author papers median 2 (systems) / 3 (theory) flags; ICRA papers 7 / 5 (see references/tone-*.md).
# Each entry is (low, high); None means unbounded on that side.
TARGETS = {
    "theory": {
        "sent_mean": (18, 25), "pct_sent_gt35": (4, 16), "pct_sent_lt12": (15, None), "para_words": (60, 115),
        "our_per_k": (None, 4.0), "our_method_per_k": (None, 0.5), "passive_per_k": (None, 12.5),
        "promo_per_k": (None, 1.5), "challenge_per_k": (None, 0.75), "to_address_per_k": (None, 0.25),
        "in_this_paper_per_k": (None, 0.6), "however_per_k": (None, 1.0), "moreover_per_k": (None, 0.9),
        "semicolon_per_k": (0.5, 6.0), "colon_per_k": (None, 12.0),  # no colon floor: mid-sentence colons are discouraged (group 15)
        "emdash_per_k": (None, 0),  # banned (SKILL.md group 10)
    },
    "systems": {
        "sent_mean": (18, 25), "pct_sent_gt35": (4, 16), "pct_sent_lt12": (12, None), "para_words": (65, 115),
        "our_per_k": (None, 4.5), "our_method_per_k": (None, 1.0), "passive_per_k": (None, 9.5),
        "promo_per_k": (None, 3.0), "challenge_per_k": (None, 1.0), "to_address_per_k": (None, 0.35),
        "in_this_paper_per_k": (None, 0.5), "however_per_k": (None, 1.0), "moreover_per_k": (None, 0.75),
        "semicolon_per_k": (0.75, 6.0), "colon_per_k": (None, 12.0),  # no colon floor (group 15)
        "emdash_per_k": (None, 0),  # banned (SKILL.md group 10)
    },
}
LABELS = {
    "sent_mean": "mean sentence length (words)", "pct_sent_gt35": "% sentences > 35 words",
    "pct_sent_lt12": "% sentences < 12 words", "para_words": "mean paragraph length (words)",
    "our_per_k": '"our"', "our_method_per_k": '"our approach/method/framework/system"',
    "passive_per_k": "passive constructions", "promo_per_k": "promotional words",
    "challenge_per_k": '"challenge(s)/challenging"', "to_address_per_k": '"to address/tackle/overcome/bridge"',
    "in_this_paper_per_k": '"in this paper/work"', "however_per_k": '"However"',
    "moreover_per_k": '"Moreover/Furthermore/Additionally/In addition"', "semicolon_per_k": "semicolons",
    "colon_per_k": "colons", "emdash_per_k": "em-dashes",
}
PATTERNS = {
    "our_per_k": (r"\bour\b", re.I),
    "our_method_per_k": (r"\bour (approach|method|framework|system)\b", re.I),
    "passive_per_k": (r"\b(is|are|was|were|be|been|being)\s+(\w+ly\s+)?\w+(ed|en|wn|lt|ught)\b", re.I),
    "promo_per_k": (r"\b(novel|significantly|significant|substantially|dramatically|remarkabl[ey]|state-of-the-art|SOTA|superior"
                    r"|unprecedented|crucial|critical|essential|vital|powerful|seamless(?:ly)?|impressive|extensive(?:ly)?"
                    r"|comprehensive(?:ly)?)\b", re.I),
    "challenge_per_k": (r"\bchallenge[sd]?\b|\bchallenging\b", re.I),
    "to_address_per_k": (r"\b[Tt]o (address|tackle|overcome|bridge)\b", 0),
    "in_this_paper_per_k": (r"\b[Ii]n this (paper|work|letter|article)\b", 0),
    "however_per_k": (r"\bHowever\b", 0),
    "moreover_per_k": (r"\b(Moreover|Furthermore|Additionally|In addition)\b", 0),
    "semicolon_per_k": (r";", 0), "colon_per_k": (r":", 0), "emdash_per_k": (r"EMDASH", 0),
}
FLAG_WORDS = r"\b(clearly|obviously|novel|state-of-the-art|SOTA|significantly|seamless(?:ly)?|unprecedented|remarkabl[ey]|paves? the way|To address this challenge)\b"
# AI-like patterns, numbered as in the "Don't write like AI!" list in SKILL.md.
AI_PATTERNS = {
    "1 AI vocabulary": r"\b(delv(?:e|es|ed|ing)|leverag(?:e|es|ed|ing)|utiliz(?:e|es|ed|ing|ation)|harness(?:es|ed|ing)?"
                       r"|underscor(?:e|es|ed|ing)|pivotal|paramount|intricate|nuanced|landscape|realm|tapestry|holistic(?:ally)?"
                       r"|foster(?:s|ed|ing)?|showcas(?:e|es|ed|ing)|streamlin(?:e|es|ed|ing)|a testament to"
                       r"|plays? an? (?:crucial|pivotal|key|vital|critical) role)\b",
    "3 trailing significance clause": r",\s+(highlighting|underscoring|demonstrating|showcasing|ensuring|emphasizing|paving)\b",
    "6 announcing instead of saying": r"\b(it is worth (noting|mentioning)|it is important to (note|emphasize|highlight)|interestingly|notably)\b",
    "8 stacked hedge": r"\b(may|might|could|can) (potentially|possibly|perhaps|conceivably)\b",
    "12 vague attribution": r"\b(studies have (shown|demonstrated|found)|researchers have|it is (widely|well|commonly) (known|accepted|recognized)"
                            r"|has been (widely|extensively) (studied|explored))\b",
    # 15: a colon inside a sentence, unless it introduces a display or a list item, or follows "as follows"
    "15 mid-sentence colon": r"(?<!follows)(?<!following):\s+(?!DISPLAYMATH|ITEM)\S",
    "16 AI-coded verb (survive; gauge for a check; charge/absorb for an operation)":
        r"\bsurviv(?:e|es|ed|ing)\b|\bgaug(?:e|es|ed|ing)\b|\bcharg(?:e|es|ed|ing)\b|\babsorb(?:s|ed|ing)?\b",
    # 19: "X is the Y that Z verbs", an object relative clause after a copula (hint; one is fine, several are not)
    "19 'is the Y that Z verbs'": r"\b(?:is|are|was|were) the (?:\w+ ){0,2}?\w+ that (?:the|a|an|its|their|each|every|our|we|it|they|this|these|one)\b",
    "18 author name as subject": r"(?-i:\b[A-Z][a-z]+(?: et al\.| and [A-Z][a-z]+)?\s*\[CITE\]\s+(?:propos|present|introduc|show|develop|extend|stud|consider|use)\w*)",
}
# 17: headers phrased as questions or as vague single words
QUESTION_HEADER = re.compile(r"\\(?:(?:sub)*section|paragraph)\*?\{((?:What|Why|How|When|Which|Does|Do|Is|Are|Can)\b[^}]*|[^}]*\?)\}")
VAGUE_HEADER = re.compile(r"\\(?:(?:sub)*section|paragraph)\*?\{(Cost|Details|Overview|Analysis|Remarks|Miscellaneous)\}")

# LaTeX: every display should be numbered (align, never align*, equation*, or \\[ \\])
UNNUMBERED_DISPLAY = re.compile(r"\\begin\{(?:align|equation|gather|multline|flalign)\*\}|(?<!\\)\\\[")
# citations without a [Sec./Thm.] pointer, checked against @book entries in the project's .bib files
CITE_CMD = re.compile(r"\\(?:cite[tp]?|parencite|autocite)\*?(\[[^\]]*\])?(?:\[[^\]]*\])?\{([^}]*)\}")
BOOK_ENTRY = re.compile(r"@(?:book|mvbook)\s*\{\s*([^,\s]+)", re.I)

UNICODE_IN_SOURCE = re.compile(r"[‘’“”–≤≥≠×→←≈±…·]")
# Group 10: em-dashes are banned in any form (---, \textemdash, a literal em-dash); en-dashes (--) are fine.
EMDASH_IN_SOURCE = re.compile(r"(?<!-)---(?!-)|\\textemdash\b|\u2014")

INPUT_RE = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
SEC_RE = re.compile(r"\\section\*?\s*(?:\[[^\]]*\])?\s*\{((?:[^{}]|\{[^{}]*\})*)\}")
DROP_ENVS = ["figure", "figure*", "table", "table*", "tikzpicture", "algorithm", "algorithm*", "algorithmic",
             "lstlisting", "verbatim", "tabular", "tabular*", "wrapfigure", "subfigure", "minipage",
             "thebibliography", "comment", "abstract"]
MATH_ENVS = ["equation", "equation*", "align", "align*", "gather", "gather*", "multline", "multline*",
             "eqnarray", "eqnarray*", "displaymath", "flalign", "flalign*"]
ABBR = r"(?<!e\.g\.)(?<!i\.e\.)(?<!et al\.)(?<!Fig\.)(?<!Eq\.)(?<!Sec\.)(?<!vs\.)(?<!resp\.)(?<!cf\.)(?<!Tab\.)(?<!Thm\.)"
SENT_SPLIT = re.compile(r"(?<=[.?!])" + ABBR + r"\s+(?=[A-Z\[(\"]|MATHX)")
SECTION_KINDS = [("intro", ["introduction"]), ("related", ["related", "prior work", "literature"]),
                 ("conclusion", ["conclusion", "limitation", "discussion", "future"]),
                 ("experiments", ["experiment", "evaluation", "result", "simulation", "hardware", "empirical", "case stud", "ablation"]),
                 ("problem", ["problem", "preliminar", "formulation", "background", "setup", "notation"])]


# Group 20 (hint): long noun phrases as subjects or objects. A heuristic on tokens, without a parser, so it misses
# some cases and flags some legitimate long subjects; read each hit.
_PREP = {"of", "in", "on", "at", "to", "from", "for", "with", "by", "through", "over", "across", "within", "between",
         "into", "onto", "among", "without", "under", "about", "along", "around", "beyond", "per", "against", "after", "before"}
_REL = {"that", "which", "who", "whose", "whom", "where"}
_AUX = {"is", "are", "was", "were", "has", "have", "had", "can", "could", "will", "would", "may", "might", "must",
        "does", "do", "did", "shall", "should"}
# Common finite verbs of technical prose (third person and past); extend as needed.
_VERBS = set("""predicts predict pushes push pushed gathers gather gathered holds hold held keeps keep kept takes take took
uses use used places place placed cuts needs need describes describe carries carry contains contain fits fit penalizes
reads read maps map gives give lies lie comes come stays stay moves move moved leaves leave left requires require rejects
reject executes execute learns learn scores score imitates trains train makes make made puts put errs overhangs presses
shows show records stands says expresses measures measure matches match reaches reach tracks track slides tilts lifts
behaves peaks beats helps flags follows starts becomes ends divides applies eases extends bounds bound grows grow
drifts decreases increases cover covers lets let reduces reduce costs cost improves improve outperforms differs
depends depend yields yield returns return remains remain falls fall rises rise
""".split())
_PRON = {"we", "it", "they", "this", "these", "those", "he", "she", "one", "i", "you"}
_CONJ = {"and", "so", "but", "or", "whereas", "while", "because", "since", "which", "where", "though", "although", "yet"}
_ADV = {"also", "still", "thus", "then", "now", "only", "never", "often", "always", "typically", "already", "therefore"}
_INTRO = {"on", "in", "with", "for", "after", "before", "when", "if", "because", "although", "though", "to", "as", "over",
          "while", "since", "unlike", "like", "among", "at", "by", "from", "under", "once", "whereas", "given", "during",
          "within", "without", "through", "across", "against", "here", "there", "still", "thus", "so", "first",
          "second", "third", "finally", "however", "instead", "then", "also", "again", "by"}


def long_noun_phrase_hints(s):
    """Return reasons why sentence s may hide a long noun phrase (group 20)."""
    out = []
    w = re.findall(r"MATHX|\[CITE\]|REF|[A-Za-z][A-Za-z'-]*|\d+(?:\.\d+)?|[,;:.]", s)
    low = [x.lower() for x in w]
    # (a) a clause used as a noun: "by how well X does", "of whether ...", "measure what ..."
    for i in range(len(low) - 1):
        if low[i] in {"by", "on", "about", "from", "of", "judge", "judges", "measure", "measures"} and \
                low[i + 1] in {"how", "what", "whether"}:
            out.append(f"a clause used as a noun ('{w[i]} {w[i + 1]} ...')")
            break
    # (b) a long subject: skip a leading phrase that ends in a comma, then count words before the main verb. A verb
    # inside a relative clause ("the mass that each density places ...") does not end the subject.
    start = 0
    if low and (low[0] in _INTRO or low[0].endswith("ing")) and "," in low[:30]:
        start = low.index(",") + 1
    if start < len(low) and low[start] not in _PRON:
        rel_open = 0
        for j in range(start, len(low)):
            x = low[j]
            if x in {";", ":", "."} or (x == "," and j + 1 < len(low) and low[j + 1] in _CONJ):
                break
            if x in _REL:
                rel_open += 1
                continue
            if x in _AUX or x in _VERBS or x in _ADV:
                if rel_open and x not in _ADV:
                    rel_open -= 1
                    continue
                subj = [y for y in low[start:j] if y not in {",", ";", ":"}]
                if len(subj) > 12 and (_REL & set(subj) or sum(y in _PREP for y in subj) >= 2):
                    out.append(f"a subject of {len(subj)} words before '{w[j]}'")
                break
    # (c) a long noun phrase after "is/are/was/were/as": to the next ; : or . (commas included)
    for i in range(len(low) - 1):
        if low[i] in {"is", "are", "was", "were", "as"} and low[i + 1] in {"the", "a", "an"}:
            span = []
            rest = low[i + 1:]
            for k, x in enumerate(rest):
                if x in {";", ":", "."} or (x == "," and k + 1 < len(rest) and rest[k + 1] in _CONJ):
                    break
                if x != ",":
                    span.append(x)
            n_prep = sum(x in _PREP for x in span)
            if len(span) >= 14 and ((_REL & set(span) and n_prep >= 2) or n_prep >= 4):
                out.append(f"a noun phrase of {len(span)} words after '{w[i]}' with {n_prep} prepositions")
                break
    return out


def inline(path, root, depth=0):
    txt = re.sub(r"(?<!\\)%.*", "", path.read_text(errors="ignore"))
    if depth > 6:
        return txt

    def rep(m):
        for base in (path.parent, root):
            for cand in (base / m.group(1).strip(), base / (m.group(1).strip() + ".tex")):
                if cand.is_file() and cand.suffix == ".tex":
                    return inline(cand, root, depth + 1)
        return ""
    return INPUT_RE.sub(rep, txt)


def find_main(target):
    if target.is_file():
        return target, target.parent
    cands = [p for p in target.rglob("*.tex") if "\\begin{document}" in p.read_text(errors="ignore")]
    if not cands:
        sys.exit(f"No .tex file with \\begin{{document}} under {target}")
    return max(cands, key=lambda p: len(inline(p, target))), target


def clean(s):
    for e in DROP_ENVS:
        s = re.sub(r"\\begin\{" + re.escape(e) + r"\}.*?\\end\{" + re.escape(e) + r"\}", " ", s, flags=re.S)
    for e in MATH_ENVS:
        s = re.sub(r"\\begin\{" + re.escape(e) + r"\}.*?\\end\{" + re.escape(e) + r"\}", " DISPLAYMATH ", s, flags=re.S)
    s = re.sub(r"\\\[.*?\\\]|\$\$.*?\$\$", " DISPLAYMATH ", s, flags=re.S)
    s = re.sub(r"(?<!\\)\$[^$]*?(?<!\\)\$|\\\(.*?\\\)", "MATHX", s, flags=re.S)
    s = re.sub(r"~?\\(?:cite[tp]?|citeauthor|parencite|autocite)\*?(\[[^\]]*\])*\{[^}]*\}", " [CITE]", s)
    s = re.sub(r"~?\\(?:[cC]ref|ref|autoref|eqref)\*?\{[^}]*\}", " REF", s)
    s = re.sub(r"\\(?:label|url|footnote|thanks|vspace|hspace|includegraphics)\*?(\[[^\]]*\])?\{[^}]*\}", " ", s)
    s = re.sub(r"\\(?:textbf|textit|emph|underline|texttt|textsc|textrm|mbox|text)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\item\b(\[[^\]]*\])?", "\n\nITEM ", s)
    s = re.sub(r"\\(?:begin|end)\{[^}]*\}", "\n\n", s)
    s = re.sub(r"\\textemdash\b(?:\{\})?|\u2014", "---", s)
    s = s.replace("---", " EMDASH ").replace("--", "-")
    s = re.sub(r"\\(?:sub)*section\*?\{[^}]*\}|\\paragraph\*?\{[^}]*\}", "\n\n", s)
    s = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}\\]", " ", s)
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*\n(\s*\n)*", "\n\n", s).strip()


def kind_of(title):
    t = title.lower()
    return next((k for k, keys in SECTION_KINDS if any(x in t for x in keys)), "method")


def body_text(main, root, section):
    full = inline(main, root)
    m = re.search(r"\\begin\{document\}(.*?)(\\end\{document\}|$)", full, re.S)
    body = m.group(1) if m else full
    body = body[:re.search(r"\\appendix\b", body).start()] if re.search(r"\\appendix\b", body) else body
    body = re.split(r"\\section\*?\{\s*Acknowledg", body)[0]
    if section:
        parts, last, cur = [], 0, "front"
        for sm in SEC_RE.finditer(body):
            if cur == section:
                parts.append(body[last:sm.start()])
            cur, last = kind_of(sm.group(1)), sm.end()
        if cur == section:
            parts.append(body[last:])
        body = "\n\n".join(parts)
    return clean(body)


def sentences(text):
    out = []
    for para in text.split("\n\n"):
        for s in SENT_SPLIT.split(para.strip()):
            if len(s.split()) >= 3:
                out.append(s.strip())
    return out


def measure(text):
    sents = sentences(text)
    lens = [len(s.split()) for s in sents]
    words = max(sum(lens), 1)
    paras = [p for p in text.split("\n\n") if len(p.split()) >= 25 and not p.startswith("ITEM")]
    m = {"words": sum(lens), "sent_mean": st.mean(lens) if lens else 0,
         "pct_sent_gt35": 100 * sum(l > 35 for l in lens) / max(len(lens), 1),
         "pct_sent_lt12": 100 * sum(l < 12 for l in lens) / max(len(lens), 1),
         "para_words": st.mean([len(p.split()) for p in paras]) if paras else 0}
    for k, (pat, flags) in PATTERNS.items():
        m[k] = 1000 * len(re.findall(pat, text, flags)) / words
    return m, sents


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("target")
    ap.add_argument("--profile", choices=["theory", "systems"], default="systems")
    ap.add_argument("--section", choices=[k for k, _ in SECTION_KINDS] + ["method"])
    a = ap.parse_args()
    main_tex, root = find_main(Path(a.target))
    text = body_text(main_tex, root, a.section)
    m, sents = measure(text)
    print(f"{main_tex}  profile={a.profile}  section={a.section or 'all'}  words={m['words']}")
    if m["words"] < 1500:
        print("note: fewer than 1,500 words; rates are noisy.")
    print(f"{'metric':48s} {'value':>7s}   target")
    flagged = 0
    for k, (lo, hi) in TARGETS[a.profile].items():
        v = m[k]
        off = (lo is not None and v < lo) or (hi is not None and v > hi)
        flagged += off
        rng = f"≥ {lo}" if hi is None else (f"≤ {hi}" if lo is None else f"{lo}–{hi}")
        print(f"{LABELS[k]:48s} {v:7.2f}   {rng:10s} {'<-- check' if off else ''}")
    print(f"\n{flagged} metric(s) outside the profile band.")
    hits = [s for s in sents if re.search(FLAG_WORDS, s, re.I)]
    if hits:
        print("\nSentences with words the profile discourages:")
        for s in hits[:15]:
            print("  -", re.sub(r"\s+", " ", s)[:200])
    ai_hits = []
    for s in sents:
        for reason in long_noun_phrase_hints(s):
            ai_hits.append(("20 long noun phrase (hint): " + reason, s))
        for name, pat in AI_PATTERNS.items():
            if re.search(pat, s, re.I) and not (name.startswith("12") and "[CITE]" in s):
                ai_hits.append((name, s))
    # 17: header levels, \\paragraph directly under a \\section that has no \\subsection
    full = re.sub(r"(?<!\\)%.*", "", inline(main_tex, root))
    for chunk in re.split(r"\\section\*?\s*(?:\[[^\]]*\])?\s*\{", full)[1:]:
        title = chunk.split("}", 1)[0]
        if "\\subsection" not in chunk and "\\paragraph" in chunk:
            ai_hits.append(("17 header level", f"\\paragraph under \\section{{{title}}} without subsections; use \\subsubsection*"))
    files = [main_tex] if Path(a.target).is_file() else sorted(Path(a.target).rglob("*.tex"))
    books = set()
    for b in Path(root).rglob("*.bib"):
        books |= set(BOOK_ENTRY.findall(b.read_text(errors="ignore")))
    for f in files:
        for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
            line = re.sub(r"(?<!\\)%.*", "", line)
            if EMDASH_IN_SOURCE.search(line):
                ai_hits.append(("10 em-dash", f"{f.name}:{i}: {line.strip()}"))
            if UNICODE_IN_SOURCE.search(line):
                ai_hits.append(("14 unicode in source", f"{f.name}:{i}: {line.strip()}"))
            if QUESTION_HEADER.search(line) or VAGUE_HEADER.search(line):
                ai_hits.append(("17 question or vague header", f"{f.name}:{i}: {line.strip()}"))
            if UNNUMBERED_DISPLAY.search(line):
                ai_hits.append(("LaTeX unnumbered display; use align", f"{f.name}:{i}: {line.strip()}"))
            for opt, keys in CITE_CMD.findall(line):
                whole = [k.strip() for k in keys.split(",") if k.strip() in books]
                if whole and not opt:
                    ai_hits.append(("whole-book citation; cite a section or theorem", f"{f.name}:{i}: {', '.join(whole)}"))
    print(f"\n{len(ai_hits)} AI-like pattern hit(s) (see \"Don't write like AI!\" in SKILL.md).")
    for name, s in ai_hits[:80]:
        print(f"  [{name}] {re.sub(r'\s+', ' ', s)[:180]}")


if __name__ == "__main__":
    main()
