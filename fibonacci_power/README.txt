# Fibonacci & Exponential Growth Benchmarking

Compares iterative vs recursive implementations of Fibonacci and exponential growth (p*(1+r)^n) across a 1,000-record self-generated dataset.

## Requirements

- Python 3.7+
- No external libraries needed (uses only `time`, `csv`, `random` from stdlib)

## How to Run

Navigate to the `fibonacci_power` folder and run:

```bash
python main.py
```

## What It Does

1. Generates `input.csv` — 1,000 Fibonacci inputs (n in [1,45]) and 1,000 power inputs (base in [1.01,1.10], exponent in [1,50])
2. Runs both iterative and recursive versions on every record, timing each
3. Prints summary tables to the console
4. Saves full results to:
   - `results_fibonacci.csv` — columns: `n, F(n), iterative_ns, recursive_ns`
   - `results_power.csv` — columns: `base, exponent, growth_value, iterative_ns, recursive_ns`

## Output Files

| File | Description |
|------|-------------|
| `input.csv` | Generated input dataset (2,000 records total) |
| `results_fibonacci.csv` | Fibonacci results with timing per record |
| `results_power.csv` | Exponential growth results with timing per record |

## Dataset Citation

Self-generated using Python's `random` module (seed=42 for reproducibility).
No external dataset source required.
