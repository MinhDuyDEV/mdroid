"""BM25 scoring for memory relevance ranking.

Port from OpenCodeKit inject.ts BM25 logic.
Stdlib only - no external dependencies.
"""

import math
from collections import Counter

try:
    from .tokenize import tokenize
except ImportError:
    from tokenize import tokenize


def bm25_score(query_terms, doc_tokens, avgdl, k1=1.5, b=0.75, doc_freq=None, n_docs=1):
    """Compute BM25 score for a single document against query terms.

    BM25 score = sum over query terms q:
        IDF(q) * (f(q, doc) * (k1 + 1)) / (f + k1 * (1 - b + b * |doc| / avgdl))

    where:
        f(q, doc) = frequency of q in doc
        |doc| = doc length (in tokens)
        avgdl = average doc length
        IDF(q) = log((N - df(q) + 0.5) / (df(q) + 0.5) + 1)
        k1 = 1.5 (term frequency saturation)
        b = 0.75 (length normalization)

    Args:
        query_terms: List of query term strings.
        doc_tokens: List of tokens in the document.
        avgdl: Average document length across the corpus.
        k1: Term frequency saturation parameter (default 1.5).
        b: Length normalization parameter (default 0.75).
        doc_freq: Dict mapping term -> document frequency (for IDF). If None,
            uses a simple IDF based on presence in query.
        n_docs: Number of documents in the corpus (for IDF).

    Returns:
        BM25 score (float).
    """
    if not query_terms or not doc_tokens:
        return 0.0
    doc_len = len(doc_tokens)
    tf = Counter(doc_tokens)
    score = 0.0
    for term in query_terms:
        f = tf.get(term, 0)
        if f == 0:
            continue
        # Compute IDF
        if doc_freq is not None and n_docs > 0:
            df = doc_freq.get(term, 0)
            idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
        else:
            # Fallback: assume each query term appears in ~half the docs
            idf = math.log(2.0)
        # BM25 term score
        numerator = f * (k1 + 1)
        denominator = f + k1 * (1 - b + b * doc_len / max(avgdl, 1))
        score += idf * (numerator / max(denominator, 1e-10))
    return score


def rank_documents(query_terms, documents, top_n=5, k1=1.5, b=0.75):
    """Rank documents by BM25 score against query terms.

    Args:
        query_terms: List of query term strings.
        documents: List of (doc_id, doc_text) tuples.
        top_n: Number of top results to return.
        k1: BM25 term frequency saturation parameter.
        b: BM25 length normalization parameter.

    Returns:
        List of (doc_id, score) tuples, sorted by score descending, top_n max.
    """
    if not query_terms or not documents:
        return []
    # Tokenize all documents
    doc_token_lists = [(doc_id, tokenize(text)) for doc_id, text in documents]
    # Compute corpus statistics
    n_docs = len(doc_token_lists)
    doc_lens = [len(tokens) for _, tokens in doc_token_lists]
    avgdl = sum(doc_lens) / max(n_docs, 1)
    # Compute document frequency for IDF
    df = Counter()
    for _, tokens in doc_token_lists:
        for term in set(tokens):
            df[term] += 1
    # Score each document
    scored = []
    for doc_id, tokens in doc_token_lists:
        score = bm25_score(
            query_terms, tokens, avgdl, k1=k1, b=b,
            doc_freq=df, n_docs=n_docs
        )
        if score > 0:
            scored.append((doc_id, score))
    # Sort by score descending, return top N
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_n]
