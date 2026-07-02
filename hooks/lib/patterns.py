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
TYPE_PATTERNS = [
    ("decision", re.compile(
        r"\b(decided to|chose to|went with|opted for|switched to|migrated to|"
        r"settled on|picked|selected|adopted)\b", re.IGNORECASE
    )),
    ("bugfix", re.compile(
        r"\b(fixed|resolved|patched|corrected|bug in|error in|crash in|"
        r"workaround for|hotfix for)\b", re.IGNORECASE
    )),
    ("pattern", re.compile(
        r"\b(pattern:|convention:|best practice|standard practice|"
        r"we always|we never|rule:|guideline:)\b", re.IGNORECASE
    )),
    ("discovery", re.compile(
        r"\b(found that|discovered|noticed|learned that|turns out|realized|"
        r"observed that|saw that)\b", re.IGNORECASE
    )),
    ("warning", re.compile(
        r"\b(warning:|caution:|careful with|gotcha|pitfall|don't use|avoid|"
        r"beware|never do|danger:|important:|note:)\b", re.IGNORECASE
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
            title = sentence.strip()
            if len(title) > 80:
                title = title[:77] + "..."
            return (obs_type, title)
    return None


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
