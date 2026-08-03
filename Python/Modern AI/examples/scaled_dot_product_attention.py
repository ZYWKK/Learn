"""Explain scaled dot-product attention with plain Python lists."""

from __future__ import annotations

import math

Matrix = list[list[float]]


def dot(left: list[float], right: list[float]) -> float:
    """Return the dot product of two equally sized vectors."""
    if len(left) != len(right):
        raise ValueError("Vectors must have the same length.")
    return sum(a * b for a, b in zip(left, right))


def softmax(values: list[float]) -> list[float]:
    """Convert scores into stable probability-like weights."""
    finite_values = [value for value in values if math.isfinite(value)]
    if not finite_values:
        raise ValueError("Softmax needs at least one finite score.")

    largest = max(finite_values)
    exponentials = [
        math.exp(value - largest) if math.isfinite(value) else 0.0
        for value in values
    ]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def scaled_dot_product_attention(
    queries: Matrix,
    keys: Matrix,
    values: Matrix,
    *,
    causal: bool = False,
) -> tuple[Matrix, Matrix]:
    """Return attention output vectors and the attention weight matrix."""
    if not queries or not keys or not values:
        raise ValueError("Queries, keys, and values cannot be empty.")
    if len(keys) != len(values):
        raise ValueError("Each key must have a matching value.")

    key_dimension = len(keys[0])
    value_dimension = len(values[0])
    if key_dimension == 0 or value_dimension == 0:
        raise ValueError("Vector dimensions must be greater than zero.")
    if any(len(query) != key_dimension for query in queries):
        raise ValueError("Every query must match the key dimension.")
    if any(len(key) != key_dimension for key in keys):
        raise ValueError("All keys must have the same dimension.")
    if any(len(value) != value_dimension for value in values):
        raise ValueError("All values must have the same dimension.")

    scale = math.sqrt(key_dimension)
    all_weights: Matrix = []
    outputs: Matrix = []

    for query_index, query in enumerate(queries):
        scores = []
        for key_index, key in enumerate(keys):
            score = dot(query, key) / scale
            if causal and key_index > query_index:
                score = -math.inf
            scores.append(score)

        weights = softmax(scores)
        output = [
            sum(weight * values[key_index][column] for key_index, weight in enumerate(weights))
            for column in range(value_dimension)
        ]
        all_weights.append(weights)
        outputs.append(output)

    return outputs, all_weights


def print_matrix(title: str, rows: Matrix) -> None:
    """Print a small matrix with aligned decimal values."""
    print(title)
    for row in rows:
        print("  " + " ".join(f"{value:7.3f}" for value in row))


def main() -> int:
    tokens = ["learn", "modern", "ai"]
    embeddings = [
        [1.0, 0.2, 0.1, 0.0],
        [0.1, 1.0, 0.3, 0.2],
        [0.0, 0.4, 1.0, 0.8],
    ]

    outputs, weights = scaled_dot_product_attention(
        embeddings,
        embeddings,
        embeddings,
        causal=True,
    )

    print("Tokens:", tokens)
    print_matrix("Causal attention weights:", weights)
    print_matrix("Context-aware output vectors:", outputs)
    print("\nEach row sums to:", [round(sum(row), 6) for row in weights])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
