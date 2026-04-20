"""
Fibonacci & Exponential Growth — Iterative vs Recursive Benchmarking

Dataset: Self-generated using Python's random module.
  - Fibonacci : 1,000 random values of n in range [1, 45]
  - Power/Growth: 1,000 random (base, exponent) pairs,
      base in [1.01, 1.10], exponent in [1, 50]
Citation: Self-generated dataset. Seed fixed at 42 for reproducibility.
"""

import time
import csv
import random

# ─── CONFIG ──────────────────────────────────────────────────────────────────

SEED            = 42
N_RECORDS       = 1000
INITIAL_P       = 1000.0
CSV_INPUT       = "input.csv"
CSV_FIB_OUT     = "results_fibonacci.csv"
CSV_POW_OUT     = "results_power.csv"
REQUIRED_FIB_NS = [10, 20, 30, 40, 45]

# ─── FIBONACCI ───────────────────────────────────────────────────────────────

def fib_iterative(n):
    """Compute nth Fibonacci number iteratively using an array."""
    if n <= 0:
        return 0
    arr = [0] * (n + 1)
    arr[1] = 1
    for i in range(2, n + 1):
        arr[i] = arr[i - 1] + arr[i - 2]
    return arr[n]


def fib_recursive(n, memo=None):
    """Compute nth Fibonacci number recursively with memoization array."""
    if memo is None:
        memo = [-1] * (n + 1)
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if memo[n] != -1:
        return memo[n]
    memo[n] = fib_recursive(n - 1, memo) + fib_recursive(n - 2, memo)
    return memo[n]

# ─── POWER / EXPONENTIAL GROWTH ──────────────────────────────────────────────

def power_iterative(base, exp):
    """Compute base^exp iteratively, storing intermediate values in array."""
    arr = [1.0] * (exp + 1)
    for i in range(1, exp + 1):
        arr[i] = arr[i - 1] * base
    return arr[exp]


def power_recursive(base, exp):
    """Compute base^exp recursively using fast exponentiation."""
    if exp == 0:
        return 1.0
    if exp == 1:
        return base
    if exp % 2 == 0:
        half = power_recursive(base, exp // 2)
        return half * half
    return base * power_recursive(base, exp - 1)


def exponential_growth(p, r, n, use_iterative=True):
    """Compute p*(1+r)^n using chosen power method."""
    if use_iterative:
        return p * power_iterative(1 + r, n)
    return p * power_recursive(1 + r, n)

# ─── DATASET GENERATION ──────────────────────────────────────────────────────

def generate_input_csv():
    rng = random.Random(SEED)

    fib_ns = REQUIRED_FIB_NS[:]
    while len(fib_ns) < N_RECORDS:
        fib_ns.append(rng.randint(1, 45))

    pow_pairs = []
    while len(pow_pairs) < N_RECORDS:
        base = round(rng.uniform(1.01, 1.10), 4)
        exp  = rng.randint(1, 50)
        pow_pairs.append((base, exp))

    with open(CSV_INPUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "n", "base", "exponent"])
        for n in fib_ns:
            writer.writerow(["fibonacci", n, "", ""])
        for base, exp in pow_pairs:
            writer.writerow(["power", "", base, exp])

    print(f"Input CSV written: {CSV_INPUT}")
    print(f"  Fibonacci records : {len(fib_ns)}")
    print(f"  Power records     : {len(pow_pairs)}")
    print(f"  Total records     : {len(fib_ns) + len(pow_pairs)}")


def read_input_csv():
    fib_inputs, pow_inputs = [], []
    with open(CSV_INPUT, newline="") as f:
        for row in csv.DictReader(f):
            if row["type"] == "fibonacci":
                fib_inputs.append(int(row["n"]))
            elif row["type"] == "power":
                pow_inputs.append((float(row["base"]), int(row["exponent"])))
    return fib_inputs, pow_inputs

# ─── TIMING HELPER ───────────────────────────────────────────────────────────

def measure(fn, *args, repeats=100):
    start = time.perf_counter_ns()
    result = None
    for _ in range(repeats):
        result = fn(*args)
    return result, (time.perf_counter_ns() - start) / repeats

# ─── TABLE PRINTER ───────────────────────────────────────────────────────────

def print_table(headers, rows):
    col_w = [max(len(str(h)), max(len(str(r[i])) for r in rows))
             for i, h in enumerate(headers)]
    sep = "+-" + "-+-".join("-" * w for w in col_w) + "-+"
    fmt = "| " + " | ".join(f"{{:<{w}}}" for w in col_w) + " |"
    print(sep)
    print(fmt.format(*headers))
    print(sep)
    for row in rows:
        print(fmt.format(*row))
    print(sep)

# ─── FIBONACCI BENCHMARK ─────────────────────────────────────────────────────

def run_fibonacci(fib_inputs):
    print("\n=== FIBONACCI — 1,000 records (n in [1,45]) ===")
    csv_rows = []
    for n in fib_inputs:
        val_i, t_i = measure(fib_iterative, n)
        val_r, t_r = measure(fib_recursive, n)
        csv_rows.append([n, val_i, round(t_i, 2), round(t_r, 2)])

    with open(CSV_FIB_OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "F(n)", "iterative_ns", "recursive_ns"])
        writer.writerows(csv_rows)

    # Console: show spec-required n values + a few extras
    display_ns = set(REQUIRED_FIB_NS + [15, 25, 35])
    seen, deduped = set(), []
    for r in csv_rows:
        if r[0] in display_ns and r[0] not in seen:
            seen.add(r[0])
            deduped.append([r[0], r[1], f"{r[2]:.1f} ns", f"{r[3]:.1f} ns"])
    deduped.sort(key=lambda x: x[0])
    print_table(["n", "F(n)", "Iterative Time", "Recursive Time"], deduped)
    print(f"Full results ({len(csv_rows)} rows) saved to {CSV_FIB_OUT}")

# ─── POWER / EXPONENTIAL GROWTH BENCHMARK ────────────────────────────────────

def run_power(pow_inputs):
    print("\n=== EXPONENTIAL GROWTH p*(1+r)^n — 1,000 records ===")
    csv_rows = []
    for base, exp in pow_inputs:
        r = base - 1.0
        val_i, t_i = measure(exponential_growth, INITIAL_P, r, exp, True)
        val_r, t_r = measure(exponential_growth, INITIAL_P, r, exp, False)
        csv_rows.append([base, exp, round(val_i, 4), round(t_i, 2), round(t_r, 2)])

    with open(CSV_POW_OUT, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["base", "exponent", "growth_value", "iterative_ns", "recursive_ns"])
        writer.writerows(csv_rows)

    step = len(csv_rows) // 12
    sample = [csv_rows[i] for i in range(0, len(csv_rows), step)][:12]
    display = [[r[0], r[1], f"{r[2]:.4f}", f"{r[3]:.1f} ns", f"{r[4]:.1f} ns"] for r in sample]
    print_table(["base", "exp", "Growth Value", "Iterative Time", "Recursive Time"], display)
    print(f"Full results ({len(csv_rows)} rows) saved to {CSV_POW_OUT}")

# ─── SUMMARY STATS ───────────────────────────────────────────────────────────

def print_summary(csv_file, label, iter_col, rec_col):
    times_i, times_r = [], []
    with open(csv_file, newline="") as f:
        for row in csv.DictReader(f):
            times_i.append(float(row[iter_col]))
            times_r.append(float(row[rec_col]))
    avg = lambda lst: sum(lst) / len(lst)
    print(f"\n--- {label} Summary (n={len(times_i)}) ---")
    print(f"{'':20s} {'Iterative':>15s} {'Recursive':>15s}")
    print(f"{'Avg time (ns)':20s} {avg(times_i):>15.1f} {avg(times_r):>15.1f}")
    print(f"{'Min time (ns)':20s} {min(times_i):>15.1f} {min(times_r):>15.1f}")
    print(f"{'Max time (ns)':20s} {max(times_i):>15.1f} {max(times_r):>15.1f}")

# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    generate_input_csv()
    fib_inputs, pow_inputs = read_input_csv()
    run_fibonacci(fib_inputs)
    run_power(pow_inputs)
    print_summary(CSV_FIB_OUT, "Fibonacci",          "iterative_ns", "recursive_ns")
    print_summary(CSV_POW_OUT, "Exponential Growth",  "iterative_ns", "recursive_ns")
