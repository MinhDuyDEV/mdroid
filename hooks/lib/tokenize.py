"""Text tokenization and stop word removal.

Port from OpenCodeKit distill.ts tokenize function.
Stdlib only - no external dependencies.
"""

import re

# English stop words + code-specific stop words.
STOP_WORDS = frozenset({
    # English stop words
    "a", "about", "above", "after", "again", "against", "all", "am", "an",
    "and", "any", "are", "aren", "as", "at", "be", "because", "been", "before",
    "being", "below", "between", "both", "but", "by", "can", "cannot", "could",
    "couldn", "did", "didn", "do", "does", "doesn", "doing", "don", "down",
    "during", "each", "few", "for", "from", "further", "had", "hadn", "has",
    "hasn", "have", "haven", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "isn", "it",
    "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor",
    "not", "now", "of", "off", "on", "once", "only", "or", "other", "our",
    "ours", "ourselves", "out", "over", "own", "s", "same", "she", "should",
    "shouldn", "so", "some", "such", "t", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was",
    "wasn", "we", "were", "weren", "what", "when", "where", "which", "while",
    "who", "whom", "why", "will", "with", "won", "would", "wouldn", "you",
    "your", "yours", "yourself", "yourselves",
    # Code stop words
    "function", "const", "let", "var", "return", "import", "export", "default",
    "class", "interface", "type", "enum", "struct", "impl", "pub", "private",
    "public", "protected", "static", "void", "null", "undefined", "true",
    "false", "none", "nil", "self", "this", "super", "new", "delete", "async",
    "await", "yield", "throw", "catch", "try", "finally", "if", "else", "elif",
    "for", "while", "loop", "break", "continue", "switch", "case", "match",
    "def", "lambda", "fn", "func", "method", "arg", "args", "param", "params",
    "obj", "obj", "arr", "str", "num", "val", "value", "item", "items",
    "index", "key", "data", "result", "res", "req", "err", "error", "callback",
    "promise", "resolve", "reject", "then", "from", "into", "use", "using",
    "get", "set", "has", "have", "make", "made", "go", "going", "went", "come",
    "came", "take", "took", "give", "gave", "find", "found", "tell", "told",
    "ask", "asked", "work", "worked", "look", "looked", "seem", "seemed",
    "feel", "felt", "try", "tried", "leave", "left", "call", "called", "want",
    "wanted", "need", "needed", "put", "let", "say", "said", "show", "showed",
    "run", "ran", "move", "moved", "live", "lived", "believe", "believed",
    "hold", "held", "bring", "brought", "happen", "happened", "write", "wrote",
    "sit", "sat", "stand", "stood", "lose", "lost", "pay", "paid", "meet",
    "met", "include", "included", "continue", "continued", "learn", "learned",
    "change", "changed", "lead", "led", "understand", "understood", "watch",
    "watched", "follow", "followed", "stop", "stopped", "create", "created",
    "speak", "spoke", "read", "allow", "allowed", "add", "added", "spend",
    "spent", "grow", "grew", "open", "opened", "walk", "walked", "win", "won",
    "offer", "offered", "remember", "remembered", "love", "loved", "consider",
    "considered", "buy", "bought", "wait", "waited", "serve", "served", "die",
    "died", "send", "sent", "expect", "expected", "build", "built", "stay",
    "stayed", "fall", "fell", "cut", "reach", "reached", "kill", "killed",
    "remain", "remained", "suggest", "suggested", "raise", "raised", "pass",
    "passed", "sell", "sold", "require", "required", "report", "reported",
    "decide", "decided", "pull", "pulled", "break", "broke", "receive",
    "received", "agree", "agreed", "hit", "produce", "produced", "eat", "ate",
    "cover", "covered", "catch", "caught", "draw", "drew", "choose", "chose",
    "point", "pointed", "save", "saved", "design", "designed", "click",
    "clicked", "involve", "involved", "tend", "tended", "raise", "raised",
    "used", "using", "able", "also", "another", "become", "became", "becomes",
    "being", "often", "less", "many", "much", "well", "way", "even", "made",
    "kind", "different", "several", "fast", "slow", "first", "last", "next",
    "main", "real", "local", "sure", "hard", "simple", "big", "small",
    "important", "long", "short", "old", "new", "good", "bad", "great", "best",
    "better", "worse", "worst", "right", "wrong", "free", "full", "empty",
    "open", "close", "closed", "start", "started", "starting", "end", "ended",
    "ending", "begin", "began", "beginning", "finish", "finished", "finishing",
})


def tokenize(text: str) -> list:
    """Tokenize text: lowercase, strip non-alphanumeric, remove stop words.

    Keeps hyphens, underscores, slashes, and dots within tokens (for paths and
    identifiers like `src/foo-bar_baz.ts`).

    Args:
        text: Input text to tokenize.

    Returns:
        List of tokens (strings), each > 2 chars, lowercased, non-stop-word.
    """
    if not text:
        return []
    # Lowercase
    text = text.lower()
    # Replace non-alphanumeric (except hyphens, underscores, slashes, dots) with space
    text = re.sub(r"[^a-z0-9_\-/.]+", " ", text)
    # Split on whitespace
    raw_tokens = text.split()
    # Filter: remove stop words, remove tokens <= 2 chars, remove pure punctuation
    tokens = [
        t for t in raw_tokens
        if len(t) > 2 and t not in STOP_WORDS and not _is_pure_punct(t)
    ]
    return tokens


def _is_pure_punct(token: str) -> bool:
    """Check if a token is pure punctuation (dots, slashes, hyphens only)."""
    return all(c in "-/._" for c in token)
