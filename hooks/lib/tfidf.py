"""TF-IDF engine for term extraction and key sentence selection.

Port from OpenCodeKit distill.ts TF-IDF functions.
Stdlib only - no external dependencies.
"""

import math
from collections import Counter

try:
    from .tokenize import tokenize
except ImportError:
    from tokenize import tokenize


def compute_tf(words: list) -> dict:
    """Compute term frequency normalized by total word count.

    Args:
        words: List of tokens.

    Returns:
        Dict mapping term -> normalized term frequency.
    """
    if not words:
        return {}
    count = Counter(words)
    total = len(words)
    return {term: freq / total for term, freq in count.items()}


def compute_idf(documents: list) -> dict:
    """Compute inverse document frequency across a set of documents.

    IDF(term) = log(N / df(term)) where N = number of documents,
    df(term) = number of documents containing the term.

    Args:
        documents: List of token lists (each document is a list of tokens).

    Returns:
        Dict mapping term -> IDF value.
    """
    n_docs = len(documents)
    if n_docs == 0:
        return {}
    df = Counter()
    for doc in documents:
        unique_terms = set(doc)
        for term in unique_terms:
            df[term] += 1
    # IDF with smoothing to avoid division by zero and log(1) = 0
    return {
        term: math.log((n_docs + 1) / (freq + 1)) + 1
        for term, freq in df.items()
    }


def extract_top_terms(messages: list, top_n: int = 20) -> list:
    """Extract top N terms by TF-IDF score across all messages.

    Treats each message as a document. Computes global TF-IDF by summing
    each term's TF across all documents weighted by IDF.

    Args:
        messages: List of message strings.
        top_n: Number of top terms to return.

    Returns:
        List of top terms (strings), ordered by score descending.
    """
    if not messages:
        return []
    # Tokenize each message into a document
    docs = [tokenize(msg) for msg in messages if msg and msg.strip()]
    if not docs:
        return []
    # Compute IDF across all documents
    idf = compute_idf(docs)
    # Compute global TF (sum of TFs across all docs)
    global_tf = Counter()
    for doc in docs:
        for term in doc:
            global_tf[term] += 1
    # Compute TF-IDF score for each term
    scores = {
        term: freq * idf.get(term, 0)
        for term, freq in global_tf.items()
    }
    # Sort by score descending, return top N
    sorted_terms = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [term for term, _ in sorted_terms[:top_n]]


def select_key_sentences(messages: list, top_terms: list, target_length: int = 2000) -> str:
    """Select key sentences using term density scoring.

    Scores each sentence by term density (how many top terms it contains)
    and greedily packs the highest-scoring sentences up to target_length chars.
    Re-sorts selected sentences by original message order for coherence.

    Args:
        messages: List of message strings.
        top_terms: List of top terms to score against.
        target_length: Maximum total character length of selected sentences.

    Returns:
        String of selected sentences, newline-separated, in original order.
    """
    if not messages or not top_terms:
        return ""
    top_term_set = set(top_terms)

    # Collect all sentences with their original order index
    import re
    sentences = []  # list of (order_index, sentence)
    order = 0
    for msg in messages:
        if not msg or not msg.strip():
            continue
        # Split into sentences: split on . ! ? followed by space or end
        raw_sentences = re.split(r"(?<=[.!?])\s+", msg.strip())
        for sent in raw_sentences:
            sent = sent.strip()
            if len(sent) < 10 or len(sent) > 500:
                continue
            sentences.append((order, sent))
            order += 1

    if not sentences:
        return ""

    # Score each sentence: term_density * (1 + term_hits)
    scored = []
    for idx, sent in sentences:
        sent_tokens = set(tokenize(sent))
        term_hits = len(sent_tokens & top_term_set)
        if term_hits == 0:
            continue
        term_density = term_hits / max(len(sent_tokens), 1)
        score = term_density * (1 + term_hits)
        scored.append((score, idx, sent))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    # Greedily pack up to target_length
    selected = []
    total_len = 0
    for score, idx, sent in scored:
        if total_len + len(sent) > target_length:
            continue
        selected.append((idx, sent))
        total_len += len(sent) + 1  # +1 for newline

    # Re-sort by original order for coherence
    selected.sort(key=lambda x: x[0])

    return "\n".join(sent for _, sent in selected)
