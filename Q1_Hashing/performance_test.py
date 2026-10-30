"""
Experiment: compare the search time of the HashTable against a 1-D array (list).
"""
import random
import time

from hash_table import HashTable
from product import Product
from inventory_system import linear_search

SIZES = [100, 1_000, 10_000, 100_000]  # number of records to test
REPEATS = 100                          # repeat single-key searches to get a stable average
RANDOM_SEARCHES = 200                  # how many random existing IDs to search per size
random.seed(42)                        # fixed seed so the experiment is reproducible


def is_prime(x):
    """Return True if x is a prime number."""
    if x < 2:
        return False
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def next_prime(n):
    """Return the smallest prime number >= n (used as the table capacity)."""
    while not is_prime(n):
        n += 1
    return n


def build_data(n):
    """Create n products with unique random IDs, stored in BOTH structures."""
    ids = random.sample(range(1, 10_000_000), n)
    products = [Product(pid, f"Medicine {pid}", "General", 10.0, 50) for pid in ids]

    table = HashTable(next_prime(2 * n))  # about half full (load factor ~0.5)
    for product in products:
        table.insert(product.product_id, product)
    return table, products


def average_ns(search_function, keys, repeats):
    """Search every key `repeats` times; return the average time per search in ns."""
    start = time.perf_counter_ns()
    for _ in range(repeats):
        for key in keys:
            search_function(key)
    total = time.perf_counter_ns() - start
    return total / (repeats * len(keys))


def main():
    print("=== Search Performance: Hash Table vs 1-D Array ===")
    print(f"{'Records':>8} | {'Case':<11} | {'Hash Table (ns)':>15} | "
          f"{'Array (ns)':>12} | {'Array / Hash':>12}")
    print("-" * 72)

    for n in SIZES:
        table, products = build_data(n)
        all_ids = [p.product_id for p in products]

        cases = {
            "First item": ([all_ids[0]], REPEATS),
            "Last item":  ([all_ids[-1]], REPEATS),
            "Not found":  ([0], REPEATS),  # IDs start at 1, so 0 never exists
            "Random avg": (random.sample(all_ids, min(RANDOM_SEARCHES, n)), 1),
        }

        for case, (keys, repeats) in cases.items():
            hash_ns = average_ns(table.search, keys, repeats)
            array_ns = average_ns(lambda k: linear_search(products, k), keys, repeats)
            print(f"{n:>8,} | {case:<11} | {hash_ns:>15,.0f} | "
                  f"{array_ns:>12,.0f} | {array_ns / hash_ns:>11.1f}x")
        print("-" * 72)


if __name__ == "__main__":
    main()