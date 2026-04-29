# CS2334 Final Project | Group 17
## Recursion vs. Iteration in Java

This repository contains our **CS2334 (Spring 2026)** final project on the practical performance trade-offs between **recursive** and **iterative** algorithm implementations in Java.

## Research Goal

The goal of this project is to determine when recursive solutions become less practical than iterative ones because of:

- JVM call stack growth
- function-call overhead
- `StackOverflowError` on large inputs

## Research Question

> At what input size does recursion's overhead make an iterative approach significantly faster or more reliable in practice?

## Algorithms Studied

We implemented both recursive and iterative versions of:

- Fibonacci Sequence
- Factorial
- Binary Search
- Fast Exponentiation (`x^n`)

## Experimental Method

For each algorithm, we benchmarked the following input sizes:

- 5,000
- 10,000
- 30,000
- 50,000
- 70,000
- 100,000

Each benchmark:

- uses `System.nanoTime()` for timing
- runs **10 times**
- averages the runtime
- records whether recursion fails with `StackOverflowError`
- exports raw data and poster-ready charts

## Current Findings

Based on the generated benchmark results in [`results/raw-data/benchmark_results.csv`](results/raw-data/benchmark_results.csv):

- **Recursive Fibonacci** completed through `30,000` and overflowed at `50,000`.
- **Recursive Factorial** completed through `30,000` and overflowed at `50,000`.
- **Binary Search** completed safely at all tested sizes; iterative search was consistently faster.
- **Fast Exponentiation** completed safely at all tested sizes; in our implementation, recursion was generally faster at the larger tested inputs.

### Recursion Cliff Summary

| Algorithm | Largest Safe Recursive Input | First Recursive Overflow |
|---|---:|---:|
| Fibonacci Sequence | 30,000 | 50,000 |
| Factorial | 30,000 | 50,000 |
| Binary Search | 100,000 | None observed |
| Fast Exponentiation | 100,000 | None observed |

## Poster Assets

The main poster figures are in [`results/charts/`](results/charts/):

- [`poster_main_runtime.svg`](results/charts/poster_main_runtime.svg): main figure showing runtime trends for all four algorithms
- [`poster_recursion_cliff.svg`](results/charts/poster_recursion_cliff.svg): figure emphasizing where recursion stops scaling safely
- [`poster_speedup_summary.svg`](results/charts/poster_speedup_summary.svg): compact comparison of recursive vs iterative runtime ratios

If the poster only uses **one** chart, use `poster_main_runtime.svg`.

## Benchmark Workflow

### Option 1: Use the Existing Results

The repository already includes:

- raw benchmark output in [`results/raw-data/`](results/raw-data/)
- averaged benchmark data in [`results/raw-data/benchmark_results.csv`](results/raw-data/benchmark_results.csv)
- poster charts in [`results/charts/`](results/charts/)
- an analysis notebook in [`results/analysis/poster_benchmarks.ipynb`](results/analysis/poster_benchmarks.ipynb)

### Option 2: Regenerate the Results

Requirements:

- Java 17+
- Python 3

Run the full benchmark and regenerate the CSV/charts:

```bash
python3 results/analysis/poster_benchmarks.py 10 1200
```

Arguments:

- `10`: number of runs per test case
- `1200`: timeout in seconds for each Java program

## Notebook Usage

The notebook at [`results/analysis/poster_benchmarks.ipynb`](results/analysis/poster_benchmarks.ipynb) can:

- load the benchmark results already saved in the repo
- regenerate the benchmark results
- display the summary table
- display the poster charts inline

Inside the notebook:

- keep `RUN_BENCHMARKS = False` to reuse the saved results
- set `RUN_BENCHMARKS = True` to rerun the Java benchmarks
- keep `NUM_RUNS = 10` for the final poster version

## Source Files

The Java implementations are in [`src/`](src/):

- [`src/FibonacciSequence.java`](src/FibonacciSequence.java)
- [`src/Factorial.java`](src/Factorial.java)
- [`src/BinarySearch.java`](src/BinarySearch.java)
- [`src/FastExponentiation.java`](src/FastExponentiation.java)

## Repository Structure

```text
.
├── bin/
│   ├── BinarySearch.class
│   ├── Factorial.class
│   ├── FastExponentiation.class
│   └── FibonacciSequence.class
├── results/
│   ├── analysis/
│   │   ├── poster_benchmarks.ipynb
│   │   └── poster_benchmarks.py
│   ├── build/
│   │   └── classes/
│   ├── charts/
│   │   ├── poster_main_runtime.svg
│   │   ├── poster_recursion_cliff.svg
│   │   └── poster_speedup_summary.svg
│   └── raw-data/
│       ├── benchmark_results.csv
│       └── *_stdout.txt
├── src/
│   ├── BinarySearch.java
│   ├── Factorial.java
│   ├── FastExponentiation.java
│   └── FibonacciSequence.java
└── README.md
```

## Project Summary

This project is an empirical study of how recursion and iteration behave differently in Java as input size grows. The main result is that recursion can remain elegant and competitive on smaller inputs, but for some algorithms it becomes less reliable at larger sizes because of stack depth limits, while iteration remains more scalable.
