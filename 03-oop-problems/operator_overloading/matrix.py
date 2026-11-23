"""Problem 7: matrix multiplication with *."""


class Matrix:
    def __init__(self, rows):
        if not rows or any(len(row) != len(rows[0]) for row in rows):
            raise ValueError("All rows must have the same length")
        self.rows = rows
        self.n_rows = len(rows)
        self.n_cols = len(rows[0])

    def __mul__(self, other):
        # (n x m) * (m x p) -> (n x p): columns of A must equal rows of B
        if self.n_cols != other.n_rows:
            raise ValueError(
                f"Cannot multiply {self.n_rows}x{self.n_cols} by {other.n_rows}x{other.n_cols}"
            )
        result = []
        for i in range(self.n_rows):
            new_row = []
            for j in range(other.n_cols):
                # result[i][j] = row i of A  ·  column j of B
                value = sum(self.rows[i][k] * other.rows[k][j] for k in range(self.n_cols))
                new_row.append(value)
            result.append(new_row)
        return Matrix(result)

    def __eq__(self, other):
        return self.rows == other.rows

    def __str__(self):
        return "\n".join(" ".join(f"{v:>4}" for v in row) for row in self.rows)

    def __repr__(self):
        return f"Matrix({self.rows})"


if __name__ == "__main__":
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    print(a * b)
    #   19   22
    #   43   50
