"""
Recursive Fibonacci function used in the Q3 experiments.
"""


def fibonacci(n):
    """Return the nth Fibonacci number using the naive recursive definition."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def count_calls(n):
    """Return how many times fibonacci() is called when computing fibonacci(n)."""
    if n <= 1:
        return 1
    return 1 + count_calls(n - 1) + count_calls(n - 2)


if __name__ == "__main__":
    # Show how the number of calls grows, to support the Big-O analysis.
    print(f"{'n':>4} | {'fibonacci(n)':>12} | {'function calls':>15} | {'growth vs n-1':>13}")
    print("-" * 54)
    previous = None
    for n in range(20, 31):
        calls = count_calls(n)
        growth = f"x{calls / previous:.3f}" if previous else "-"
        print(f"{n:>4} | {fibonacci(n):>12,} | {calls:>15,} | {growth:>13}")
        previous = calls