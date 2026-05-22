# OCPT Conformance Checking

A Python framework for **conformance checking of Object-Centric Process Trees (OCPTs)** against Object-Centric Event Logs (OCELs). This repository implements an abstraction-based conformance checking approach and benchmarks it against three established baseline methods: perspective-based, context-based, and alignment-based conformance checking.

---

## Overview

Object-Centric Process Mining generalises classical process mining by allowing events to relate to multiple objects of different types simultaneously. This project provides:

- An **abstraction-based conformance checker** for OCPTs that decomposes conformance into three dimensions: **control flow**, **multiplicity**, and **identity**.
- A **fitness** and **precision** implementation for OCPT abstractions.
- Benchmarking infrastructure comparing the abstraction approach against:
  - **Perspective-based** conformance (via `park`)
  - **Context-based** conformance (via `adams`)
  - **Alignment-based** conformance (via `liss` / OC-alignments)
- An `example.py` demonstrating how to construct an OCPT and run conformance checking from scratch.

---

## Repository Structure

```
OCPT-Conformance-Checking/
├── src/                        # Core implementation
│   ├── oc_process_trees.py     # OCPT data structures (OperatorNode, LeafNode, Operator)
│   ├── conformance.py          # Conformance checking: determine_conformance, get_fitness, get_precision
│   ├── log_abstraction.py      # Log abstraction computation
│   ├── tree_abstraction.py     # Tree abstraction computation
│   └── ...                     # DF2 miner, OCPN conversion utilities
├── adams/                      # Context-based baseline (Adams et al.)
├── liss/                       # Alignment-based baseline (OC-alignments)
├── park/                       # Perspective-based baseline
├── data/                       # OCEL input logs (.jsonocel / .ocel2)
├── example.py                  # Minimal worked example from the paper
├── main.py                     # Full benchmark runner
├── fast_hash.pyx               # Cython extension for performance-critical hashing
├── fast_hash.c                 # Generated C source for fast_hash
├── setup.py                    # Build script for the Cython extension
├── comparison.csv              # Fitness/precision comparison results
├── result_abstraction.csv      # Abstraction-based runtime results
├── result_perspective.csv      # Perspective-based runtime results
└── result_context.csv          # Context-based runtime results
```

---

## Installation

### Prerequisites

- Python 3.10+
- A C compiler (for building the Cython extension)

### Steps

1. **Clone the repository**

   ```bash
   git clonelink-to-repo
   cd OCPT-Conformance-Checking
   ```

2. **Install dependencies**

   ```bash
   pip install pm4py pandas numpy cython
   ```

3. **Build the Cython extension** (required for performance)

   ```bash
   python setup.py build_ext --inplace
   ```

   This compiles `fast_hash.pyx` into a native extension used to accelerate state hashing during conformance checking.

---

## Quick Start

The `example.py` file demonstrates how to manually construct an OCPT and run conformance checking on a small log from the paper:

```python
from src.oc_process_trees import OperatorNode, LeafNode, Operator
from src.conformance import determine_conformance

# Define leaf nodes with object type annotations
place  = LeafNode(activity="place",  related={"c","o","i"}, divergent={"c"}, convergent={"i"}, deficient=set())
pay    = LeafNode(activity="pay",    related={"c","o","i"}, divergent={"c"}, convergent={"i"}, deficient=set())
pack   = LeafNode(activity="pack",   related={"o","i"},     divergent=set(), convergent={"i"}, deficient=set())
refund = LeafNode(activity="refund", related={"c","o","i"}, divergent={"c"}, convergent={"i"}, deficient=set())
pickup = LeafNode(activity="pickup", related={"c","o","i"}, divergent={"c"}, convergent={"i"}, deficient=set())

# Build the process tree
ocpt = OperatorNode(Operator.SEQUENCE, [
    place,
    OperatorNode(Operator.PARALLEL, [pay, pack]),
    OperatorNode(Operator.XOR, [refund, pickup])
])

# Run conformance checking with a 10-second timeout
determine_conformance(ocpt, relations, timeout=10)
```

Run it with:

```bash
python example.py
```

---

## Running the Full Benchmark

Place your OCEL log files (`.jsonocel` or `.ocel2` format) in the `data/` directory, then run:

```bash
python main.py
```

By default this runs the **abstraction-based** approach with a 1-hour budget per log and writes results to `result_abstraction.csv`. The other approaches (perspective, context, alignment) are commented out in `main.py` as they tend to time out on larger logs even with extended budgets.

To enable them, uncomment the relevant lines in the `if __name__ == "__main__":` block:

```python
budget = 3600
run_abstractions(budget)
# run_perspective(budget)
# run_context(budget)
# run_alignment(budget)
```

### Output Files

| File | Contents |
|---|---|
| `result_abstraction.csv` | Runtime, timeout rate, and time breakdown (control / multiplicity / identity / overhead) per log |
| `result_perspective.csv` | Runtime and timeout rate for perspective-based checking |
| `result_context.csv` | Runtime and timeout rate for context-based checking |
| `result_alignment.csv` | Runtime and timeout rate for alignment-based checking |
| `comparison.csv` | Side-by-side fitness and precision scores (abstraction vs. perspective) |

---

## Conformance Dimensions

The abstraction-based approach decomposes conformance into three independently measurable dimensions:

| Dimension | Description |
|---|---|
| **Control** | Whether the ordering and branching of activities matches the process tree structure |
| **Multiplicity** | Whether the number of object interactions per event matches model expectations |
| **Identity** | Whether the specific object identifiers involved in events are consistent across the trace |

---

## Dependencies

| Package | Purpose |
|---|---|
| `pm4py` | Reading OCEL logs, Petri net operations, alignment-based metrics |
| `pandas` | Event log manipulation |
| `numpy` | Numerical aggregation |
| `cython` | Compiling `fast_hash.pyx` for efficient state hashing |

---

## Baseline Methods

The three baseline conformance checkers included for comparison are:

- **`park/`** — Perspective-based conformance: projects the object-centric log onto per-object-type Petri nets and checks each independently.
- **`adams/`** — Context-based conformance: checks events in their local object context.
- **`liss/`** — Alignment-based conformance: computes optimal object-centric alignments using the OC-alignment framework.
