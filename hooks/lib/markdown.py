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
