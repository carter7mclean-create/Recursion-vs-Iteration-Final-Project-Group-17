# CS2334 Final Project || Group 17
## Recursion vs. Iteration in Java

This repository contains our team’s final project for **CS2334 (Spring 2026)**. The goal of this project is to investigate the practical performance trade-offs between **recursive** and **iterative** implementations of common algorithms in Java, with a focus on identifying when recursion becomes inefficient due to JVM call stack overhead.

## Link to Poster:
(will post here) but before so discuss about a templete

## Project Question

> At what input size does the overhead of recursion make an iterative approach significantly more efficient in practice?

## Project Overview

Recursion is often elegant and easier to read, but it uses the JVM call stack and can introduce extra overhead through repeated method calls. Iteration is usually more memory-efficient and avoids deep stack growth, though it can sometimes be less intuitive to write. This project compares both approaches experimentally.

## Algorithms Covered

Our team implemented both **recursive** and **iterative** versions of the following algorithms:

- Fibonacci Sequence
- Factorial
- Binary Search
- Fast Exponentiation (`x^n`)

## Experimental Method

For each algorithm, we run performance tests using these input sizes:

- 5,000
- 10,000
- 30,000
- 50,000
- 70,000
- 100,000

Each test:

- records runtime using `System.nanoTime()`
- runs at least 10 times
- averages results for fairness
- checks for the recursion cliff, where the recursive version throws `StackOverflowError`
- compares runtime trends using graphs and charts

## Repository Structure

(TEAM must approved below structure, otherwise no changes can made)

```text
.
├── bin/
│   ├── BinarySearch.class
│   ├── Factorial.class
│   ├── FastExponentiation.class
│   └── FibonacciSequence.class
│
├── src/
│   ├── BinarySearch.java
│   ├── Factorial.java
│   ├── FastExponentiation.java
│   └── FibonacciSequence.java
│
├── results/
│   ├── raw-data/
│   ├── charts/
│   └── analysis/
│
├── docs/
│   ├── literature-review.md
│   ├── methodology.md
│   └── conclusions.md
│
├── .classpath
├── .project
└── README.md
