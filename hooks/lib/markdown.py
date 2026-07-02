"""Memory markdown file helpers: parse, append, dedup.

Stdlib only - no external dependencies.
"""

import os
from datetime import datetime


def read_memories(path: str) -> list:
    """Parse a memories.md file into a list of observation dicts.

    Each observation block has the format:
        ### [YYYY-MM-DD]: [Title]
        **Type**: decision/bugfix/pattern/discovery/warning
        **Confidence**: high/medium/low
        **Content**: [content text]
        **Concepts**: [concept1, concept2, ...]

    Args:
        path: Path to memories.md file.

    Returns:
        List of dicts with keys: date, title, type, confidence, content, concepts.
    """
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text.strip():
        return []
    observations = []
    # Normalize: ensure text starts with "### " so split captures the first block.
    # Without this, the first observation (which starts with "### ") is lost
    # because split on "\n### " treats it as a prefix, not a delimiter.
    if not text.startswith("\n### "):
        if text.startswith("### "):
            text = "\n" + text
        else:
            # Lines not starting with "### " are legacy manual entries; skip them.
            # But find the first "### " line and prepend a newline before it.
            idx = text.find("\n### ")
            if idx == -1:
                return []
            text = text[:idx] + "\n" + text[idx + 1:]
    # Split on "\n### " so every block (including the first) starts with "[date]: title"
    blocks = text.split("\n### ")
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        obs = _parse_block(block)
        if obs:
            observations.append(obs)
    return observations


def _parse_block(block: str) -> dict:
    """Parse a single observation block into a dict."""
    lines = block.strip().split("\n")
    if not lines:
        return None
    header = lines[0].strip()
    # Header format: [YYYY-MM-DD]: [Title]
    # Handle both with and without leading brackets
    header_match = None
    import re
    m = re.match(r"\[?(\d{4}-\d{2}-\d{2})\]?\s*:\s*(.+)", header)
    if not m:
        return None
    date = m.group(1)
    title = m.group(2).strip()
    obs = {
        "date": date,
        "title": title,
        "type": "unknown",
        "confidence": "medium",
        "content": "",
        "concepts": [],
    }
    # Parse metadata lines
    content_lines = []
    in_content = False
    for line in lines[1:]:
        line = line.strip()
        if line.startswith("**Type**:"):
            obs["type"] = line.replace("**Type**:", "").strip()
        elif line.startswith("**Confidence**:"):
            obs["confidence"] = line.replace("**Confidence**:", "").strip()
        elif line.startswith("**Content**:"):
            obs["content"] = line.replace("**Content**:", "").strip()
            in_content = True
        elif line.startswith("**Concepts**:"):
            concepts_raw = line.replace("**Concepts**:", "").strip()
            obs["concepts"] = [
                c.strip().strip("[]")
                for c in concepts_raw.split(",")
                if c.strip().strip("[]")
            ]
            in_content = False
        elif in_content and line:
            content_lines.append(line)
    if content_lines:
        obs["content"] = obs["content"] + " " + " ".join(content_lines)
    return obs


def append_observation(path: str, observation: dict) -> None:
    """Append a formatted observation block to memories.md.

    Args:
        path: Path to memories.md file.
        observation: Dict with keys: type, title, content, concepts, confidence, date.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(path) else None
    block = _format_block(observation)
    with open(path, "a", encoding="utf-8") as f:
        f.write(block + "\n")


def _format_block(obs: dict) -> str:
    """Format an observation dict into a markdown block."""
    date = obs.get("date") or datetime.now().strftime("%Y-%m-%d")
    title = obs.get("title", "Untitled").strip()
    obs_type = obs.get("type", "unknown")
    confidence = obs.get("confidence", "medium")
    content = obs.get("content", "").strip()
    concepts = obs.get("concepts", [])
    concepts_str = ", ".join(concepts) if concepts else ""
    lines = [
        f"### [{date}]: {title}",
        f"**Type**: {obs_type}",
        f"**Confidence**: {confidence}",
        f"**Content**: {content}",
    ]
    if concepts_str:
        lines.append(f"**Concepts**: [{concepts_str}]")
    return "\n".join(lines)


def is_duplicate(title: str, existing_titles: set, prefix_len: int = 40) -> bool:
    """Check if a title is a duplicate of an existing one (fuzzy prefix match).

    Comparison is case-insensitive on the first `prefix_len` characters.

    Args:
        title: The title to check.
        existing_titles: Set of existing titles (already lowercased for
            case-insensitive comparison).
        prefix_len: Number of chars to compare for prefix matching.

    Returns:
        True if duplicate, False otherwise.
    """
    title_prefix = title.strip().lower()[:prefix_len]
    for existing in existing_titles:
        if existing.strip().lower()[:prefix_len] == title_prefix:
            return True
    return False


def get_existing_titles(path: str) -> set:
    """Get all existing observation titles from memories.md.

    Args:
        path: Path to memories.md file.

    Returns:
        Set of lowercased title strings for case-insensitive dedup.
    """
    observations = read_memories(path)
    return {obs["title"].lower() for obs in observations}


def get_existing_contents(path: str) -> set:
    """Get all existing observation contents (normalized) for dedup.

    Normalization lowercases, collapses whitespace, and strips backticks so
    that content that differs only in spacing, case, or markdown backticks is
    treated as a duplicate. This catches garbage re-ingestions where the same
    sentence appears with slightly different leading context (e.g. different
    "(relevance: N)" prefixes).

    Args:
        path: Path to memories.md file.

    Returns:
        Set of normalized content strings.
    """
    import re as _re
    observations = read_memories(path)
    normalized = set()
    for obs in observations:
        c = obs.get("content", "").strip().lower()
        c = _re.sub(r"\s+", " ", c)
        if c:
            normalized.add(c)
    return normalized


def is_content_duplicate(content: str, existing_contents: set, prefix_len: int = 60) -> bool:
    """Check if content is a duplicate of an existing observation content.

    Comparison is case-insensitive, whitespace-normalized, and backtick-stripped
    on the first `prefix_len` characters. Backtick stripping matters because the
    same sentence can be stored with or without markdown backticks (e.g. when
    re-ingested from rendered hook output vs. genuine assistant prose). This
    catches the self-reinforcing corruption loop where injected memory context
    gets re-ingested with slightly different leading context but the same core
    sentence.

    Args:
        content: The content to check.
        existing_contents: Set of normalized existing content strings.
        prefix_len: Number of chars to compare for prefix matching.

    Returns:
        True if duplicate, False otherwise.
    """
    import re as _re
    norm = _re.sub(r"\s+", " ", content.strip().lower())
    norm = norm.replace("`", "")
    prefix = norm[:prefix_len]
    if not prefix:
        return False
    for existing in existing_contents:
        if existing.replace("`", "")[:prefix_len] == prefix:
            return True
    return False
