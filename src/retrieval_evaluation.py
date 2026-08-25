from typing import Sequence


def precision_at_k(
    retrieved: Sequence[str],
    relevant: set[str],
    k: int,
) -> float:
    """
    Calculate Precision@K.
    """

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    top_k = list(retrieved[:k])

    if not top_k:
        return 0.0

    relevant_retrieved = sum(
        1
        for item in top_k
        if item in relevant
    )

    return relevant_retrieved / len(top_k)


def recall_at_k(
    retrieved: Sequence[str],
    relevant: set[str],
    k: int,
) -> float:
    """
    Calculate Recall@K.
    """

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if not relevant:
        return 0.0

    top_k = list(retrieved[:k])

    relevant_retrieved = sum(
        1
        for item in top_k
        if item in relevant
    )

    return relevant_retrieved / len(relevant)

def reciprocal_rank(
    retrieved: Sequence[str],
    relevant: set[str],
) -> float:
    """
    Calculate Reciprocal Rank for one ranked result list.
    """

    for rank, item in enumerate(retrieved, start=1):
        if item in relevant:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    ranked_results: Sequence[Sequence[str]],
    relevant_sets: Sequence[set[str]],
) -> float:
    """
    Calculate Mean Reciprocal Rank across multiple queries.
    """

    if len(ranked_results) != len(relevant_sets):
        raise ValueError(
            "ranked_results and relevant_sets must have the same length."
        )

    if not ranked_results:
        return 0.0

    scores = [
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant in zip(
            ranked_results,
            relevant_sets,
        )
    ]

    return sum(scores) / len(scores)

import math


def dcg_at_k(
    relevance_scores: Sequence[float],
    k: int,
) -> float:
    """
    Calculate Discounted Cumulative Gain at K.
    """

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    top_k = list(relevance_scores[:k])

    return sum(
        score / math.log2(rank + 1)
        for rank, score in enumerate(top_k, start=1)
    )


def ndcg_at_k(
    relevance_scores: Sequence[float],
    k: int,
) -> float:
    """
    Calculate Normalized Discounted Cumulative Gain at K.
    """

    actual_dcg = dcg_at_k(
        relevance_scores,
        k,
    )

    ideal_scores = sorted(
        relevance_scores,
        reverse=True,
    )

    ideal_dcg = dcg_at_k(
        ideal_scores,
        k,
    )

    if ideal_dcg == 0:
        return 0.0

    return actual_dcg / ideal_dcg

def reciprocal_rank_at_k(
    retrieved: Sequence[str],
    relevant: set[str],
    k: int,
) -> float:
    """
    Calculate Reciprocal Rank using only the top K results.
    """

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    return reciprocal_rank(
        retrieved[:k],
        relevant,
    )


def mean_reciprocal_rank_at_k(
    ranked_results: Sequence[Sequence[str]],
    relevant_sets: Sequence[set[str]],
    k: int,
) -> float:
    """
    Calculate Mean Reciprocal Rank using only the top K results.
    """

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if len(ranked_results) != len(relevant_sets):
        raise ValueError(
            "ranked_results and relevant_sets must have the same length."
        )

    if not ranked_results:
        return 0.0

    scores = [
        reciprocal_rank_at_k(
            retrieved,
            relevant,
            k,
        )
        for retrieved, relevant in zip(
            ranked_results,
            relevant_sets,
        )
    ]

    return sum(scores) / len(scores)

def evaluate_retrieval_at_k(
    retrieved: Sequence[str],
    relevant: set[str],
    relevance_scores: Sequence[float],
    k: int,
) -> dict[str, float]:
    """
    Return the core retrieval-quality metrics for one query at K.
    """

    return {
        "precision_at_k": precision_at_k(
            retrieved,
            relevant,
            k,
        ),
        "recall_at_k": recall_at_k(
            retrieved,
            relevant,
            k,
        ),
        "reciprocal_rank_at_k": reciprocal_rank_at_k(
            retrieved,
            relevant,
            k,
        ),
        "ndcg_at_k": ndcg_at_k(
            relevance_scores,
            k,
        ),
    }