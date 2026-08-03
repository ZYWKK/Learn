"""Show the forward-pass idea behind LoRA with small matrices."""

from __future__ import annotations

Matrix = list[list[float]]


def matrix_shape(matrix: Matrix) -> tuple[int, int]:
    """Return matrix rows and columns after validating its shape."""
    if not matrix or not matrix[0]:
        raise ValueError("Matrix cannot be empty.")
    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError("Matrix rows must have the same length.")
    return len(matrix), column_count


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    """Multiply two small dense matrices."""
    left_rows, left_columns = matrix_shape(left)
    right_rows, right_columns = matrix_shape(right)
    if left_columns != right_rows:
        raise ValueError("Inner matrix dimensions must match.")

    return [
        [
            sum(left[row][inner] * right[inner][column] for inner in range(left_columns))
            for column in range(right_columns)
        ]
        for row in range(left_rows)
    ]


def matrix_vector_multiply(matrix: Matrix, vector: list[float]) -> list[float]:
    """Multiply a matrix by one input vector."""
    _, column_count = matrix_shape(matrix)
    if column_count != len(vector):
        raise ValueError("Vector length must match matrix columns.")
    return [sum(weight * value for weight, value in zip(row, vector)) for row in matrix]


def apply_lora(
    base_weight: Matrix,
    lora_a: Matrix,
    lora_b: Matrix,
    *,
    alpha: float,
) -> tuple[Matrix, Matrix]:
    """Return W + scale * (B @ A) and the scaled low-rank update."""
    rank, input_size = matrix_shape(lora_a)
    output_size, b_rank = matrix_shape(lora_b)
    base_rows, base_columns = matrix_shape(base_weight)
    if b_rank != rank:
        raise ValueError("LoRA A and B must use the same rank.")
    if (base_rows, base_columns) != (output_size, input_size):
        raise ValueError("LoRA update must match the base weight shape.")

    scale = alpha / rank
    raw_update = matrix_multiply(lora_b, lora_a)
    scaled_update = [[scale * value for value in row] for row in raw_update]
    adapted_weight = [
        [base + delta for base, delta in zip(base_row, update_row)]
        for base_row, update_row in zip(base_weight, scaled_update)
    ]
    return adapted_weight, scaled_update


def main() -> int:
    base_weight = [
        [0.40, -0.20, 0.10, 0.30],
        [0.10, 0.50, -0.40, 0.20],
        [-0.30, 0.20, 0.60, 0.10],
    ]
    lora_a = [
        [0.10, -0.20, 0.05, 0.15],
    ]
    lora_b = [
        [0.30],
        [-0.20],
        [0.10],
    ]
    input_vector = [1.0, 0.5, -0.5, 0.2]

    adapted_weight, update = apply_lora(base_weight, lora_a, lora_b, alpha=1.0)
    base_output = matrix_vector_multiply(base_weight, input_vector)
    adapted_output = matrix_vector_multiply(adapted_weight, input_vector)

    output_size, input_size = matrix_shape(base_weight)
    rank, _ = matrix_shape(lora_a)
    full_parameter_count = output_size * input_size
    lora_parameter_count = rank * (input_size + output_size)

    print(f"Full weight parameters: {full_parameter_count}")
    print(f"LoRA trainable parameters: {lora_parameter_count}")
    print("Scaled low-rank update:")
    for row in update:
        print("  " + " ".join(f"{value:7.3f}" for value in row))
    print("Base output:   ", [round(value, 4) for value in base_output])
    print("Adapted output:", [round(value, 4) for value in adapted_output])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
