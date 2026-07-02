"""Regex pattern matching for observation extraction.

Port from OpenCodeKit curator.ts CURATOR_PATTERNS.
Stdlib only - no external dependencies.
"""

import re

try:
    from .tokenize import tokenize
except ImportError:
    from tokenize import tokenize


# (type, compiled_regex) tuples for matching observation sentences.
# Keywords are English + Vietnamese to support multilingual sessions.
# Note: \b word boundary is unreliable with accented Vietnamese characters
# (Python \b treats them as word chars, but boundary detection is inconsistent
# across regex engines). For Vietnamese keywords, we use lookahead/lookbehind
# for whitespace/punctuation instead of \b.
# For colon-terminated English keywords (warning:, note:), no trailing \b
# because \b requires a word char on both sides and ":" is non-word.
_VI_BOUNDARY = r"(?:\s|$|[,.;!?:])"

TYPE_PATTERNS = [
    ("decision", re.compile(
        r"\b(decided to|chose to|went with|opted for|switched to|migrated to|"
        r"settled on|picked|selected|adopted)\b"
        r"|(?:quyết định|chọn|chấp nhận|lựa chọn)(?=" + _VI_BOUNDARY + r")",
        re.IGNORECASE
    )),
    ("bugfix", re.compile(
        r"\b(fixed|resolved|patched|corrected|bug in|error in|crash in|"
        r"workaround for|hotfix for)\b"
        r"|(?:khắc phục|sửa|chữa lỗi|tái chính)(?=" + _VI_BOUNDARY + r")",
        re.IGNORECASE
    )),
    ("pattern", re.compile(
        r"\b(best practice|standard practice|we always|we never)\b"
        r"|\b(pattern|convention|rule|guideline)(?=\s*:)"
        r"|(?:luật|quy tắc|chuẩn mực|luôn luôn)(?=" + _VI_BOUNDARY + r")",
        re.IGNORECASE
    )),
    ("discovery", re.compile(
        r"\b(found that|discovered|noticed|learned that|turns out|realized|"
        r"observed that|saw that)\b"
        r"|(?:phát hiện|thấy rằng|nhận ra|tìm ra)(?=" + _VI_BOUNDARY + r")",
        re.IGNORECASE
    )),
    ("warning", re.compile(
        r"\b(warning|caution|careful with|gotcha|pitfall|"
        r"don't use|avoid|beware|never do|danger|important|note)"
        r"(?=\s*:)"
        r"|(?:cảnh báo|cẩn thận|tránh|không dùng|không sử dụng)(?=" + _VI_BOUNDARY + r")",
        re.IGNORECASE
    )),
]


def match_patterns(sentence: str):
    """Match a sentence against curator patterns.

    Args:
        sentence: Input sentence string.

    Returns:
        (type, title) tuple if matched, or None if no pattern matches.
        Title is the sentence truncated to 80 chars.
    """
    if not sentence or len(sentence) < 10:
        return None
    for obs_type, pattern in TYPE_PATTERNS:
        if pattern.search(sentence):
            title = _truncate_title(sentence.strip(), max_len=80)
            return (obs_type, title)
    return None


def _truncate_title(title: str, max_len: int = 80) -> str:
    """Truncate a title to max_len chars, cutting at a word boundary.

    If the title fits within max_len, return it unchanged.
    Otherwise, find the last word boundary at or before max_len and append '...'.
    Never cuts a word in half (the original implementation cut mid-token, e.g.
    'custom:` + fi...' instead of 'custom:` + field...').

    Args:
        title: The candidate title (already stripped).
        max_len: Maximum allowed length including the '...' suffix.

    Returns:
        The truncated title ending in '...' if it was too long, else the
        original title.
    """
    if len(title) <= max_len:
        return title
    # Reserve 3 chars for the '...' suffix.
    budget = max_len - 3
    # Find the last whitespace at or before the budget so we don't split a word.
    cut = title.rfind(" ", 0, budget + 1)
    if cut <= 0:
        # No whitespace in range: fall back to a hard cut (e.g. a single long
        # token like a path or identifier).
        cut = budget
    return title[:cut].rstrip() + "..."


def extract_concepts(sentence: str, max_concepts: int = 5) -> list:
    """Extract significant concept words from a sentence.

    Uses tokenize to get meaningful terms, returns up to max_concepts.

    Args:
        sentence: Input sentence string.
        max_concepts: Maximum number of concept terms to return.

    Returns:
        List of concept term strings.
    """
    tokens = tokenize(sentence)
    # Deduplicate while preserving order
    seen = set()
    concepts = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            concepts.append(t)
            if len(concepts) >= max_concepts:
                break
    return concepts
