"""
Q3: Calculate Fibonacci(35), Fibonacci(38) and Fibonacci(40) with and without
multithreading over several rounds, and compare the time taken.
"""
import platform
import sys
import threading
import time

from fibonacci import fibonacci

NUMBERS = [35, 38, 40]
ROUNDS = 10 # change to 2 for a quick test; use 10 for the final results
WIDTH = 90


def worker(n, results, start_times, end_times, lock):
    """Thread task: calculate fibonacci(n) and record when it started and ended."""
    start = time.perf_counter_ns()
    value = fibonacci(n)
    end = time.perf_counter_ns()
    with lock:  # only one thread may update the shared dictionaries at a time
        results[n] = value
        start_times[n] = start
        end_times[n] = end


def run_with_threads():
    """One round with a separate thread per number. Returns (results, T in ns)."""
    results, start_times, end_times = {}, {}, {}
    lock = threading.Lock()

    threads = [
        threading.Thread(target=worker, args=(n, results, start_times, end_times, lock))
        for n in NUMBERS
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()  # wait until every thread has finished

    # T = end time of the thread that finished LAST - start time of the thread that started FIRST
    elapsed = max(end_times.values()) - min(start_times.values())
    return results, elapsed


def run_without_threads():
    """One round calculating the numbers one after another. Returns (results, T in ns)."""
    results = {}
    start = time.perf_counter_ns()
    for n in NUMBERS:
        results[n] = fibonacci(n)
    elapsed = time.perf_counter_ns() - start
    return results, elapsed


def run_experiment(title, run_round):
    """Run `run_round` for ROUNDS rounds, print each T and return the average T."""
    print("=" * WIDTH)
    print(title.center(WIDTH))
    print("=" * WIDTH)

    times = []
    for round_number in range(1, ROUNDS + 1):
        results, elapsed = run_round()
        times.append(elapsed)
        values = ", ".join(f"Fib({n})={results[n]}" for n in NUMBERS)
        print(f"Round {round_number:>2}: {values} | T = {elapsed:,} ns")

    average = sum(times) / len(times)
    print("-" * WIDTH)
    print(f"Average T: {average:,.0f} ns  ({average / 1e9:.2f} seconds)\n")
    return average


def main():
    gil_enabled = getattr(sys, "_is_gil_enabled", lambda: True)()
    print(f"Python {platform.python_version()} | GIL enabled: {gil_enabled} | "
          f"Rounds: {ROUNDS} | Numbers: {NUMBERS}")
    print("Please wait - this experiment takes several minutes.\n")

    with_threads = run_experiment("FIBONACCI COMPUTATION (WITH MULTITHREADING)",
                                  run_with_threads)
    without_threads = run_experiment("FIBONACCI COMPUTATION (WITHOUT MULTITHREADING)",
                                     run_without_threads)

    difference = (without_threads - with_threads) / without_threads * 100
    print("=" * WIDTH)
    print(f"Average with multithreading    : {with_threads:,.0f} ns")
    print(f"Average without multithreading : {without_threads:,.0f} ns")
    if abs(difference) < 2:
        print(f"Observation: difference of {abs(difference):.1f}% is within measurement "
              "noise - multithreading gave no real speed-up.")
    elif difference > 0:
        print(f"Observation: multithreading was {difference:.1f}% FASTER on average.")
    else:
        print(f"Observation: multithreading was {-difference:.1f}% SLOWER on average.")


if __name__ == "__main__":
    main()