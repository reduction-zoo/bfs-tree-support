# BFS tree support → Horn satisfiability

This Lake package defines the actual board question, not a proposed solution.
`Challenge.lean` is the standalone Comparator statement: it imports only Mathlib,
fixes the two problems, their finite encodings, NO-SOLUTION semantics and the
exact reduction goal, and states the open theorem `BFSTreeSupport.solve`.
`Solution.lean` is its unfilled starting copy.

## Fixed meaning

A source is a nonempty list of permutations of the same nonempty vertex set
`0,…,n−1`. A positive output is one simple tree on that vertex set supporting
every permutation as an ordinary FIFO breadth-first traversal. Different orders
may start at different roots and choose different neighbor tie orders. Merely
respecting distance layers is insufficient: a queued parent's children must be
discovered before those of a later queued parent. Edges may be listed in either
orientation; duplicate unordered edges and loops are illegal.

A target is a finite Horn CNF with zero-based variable indices. Every clause has
at most one positive literal occurrence. Empty clauses and repeated literals are
permitted, as in the prepared input contract. A positive output assigns exactly
one Boolean to each variable and satisfies every clause. On each side,
`none` means that no accepted positive witness exists, not that execution failed.

`Goal` asks for two unknown functions: a construction from profiles to Horn
formulas and recovery from a profile together with any valid Horn output.
`Reduction` requires legal target construction and valid source recovery for
every legal profile and every valid target output, including alternate assignments
and NO-SOLUTION. It also requires polynomial time in Mathlib's finite-alphabet
stack Turing-machine model and polynomial output length for both maps. Time and
length are measured on explicit self-delimiting binary encodings. Recovery's
input is the full pair of source instance and target output.

The goal does not assume a proposed reduction, propagation completeness,
extractability, or any extra restriction on the admitted profiles. It follows the
fixed campaign's preprocessing/recovery contract; it adds no requirement of a
bijection or raw equality between source and target answers.

## Build and inspect

Lean 4.34.0 and the exact Mathlib revision are pinned by `lean-toolchain`,
`lakefile.toml` and `lake-manifest.json`. In this directory:

```sh
lake exe cache get Mathlib.Computability.TuringMachine.Computable
LEAN_NUM_THREADS=2 lake build
lake env lean Audit.lean
```

Only the two open theorem placeholders should report `sorry`. The definitions
and `Goal` have no proof holes. Compilation and semantic tests establish a
well-formed specification, not a solution of the open question.

## Submit a solution to Comparator

Keep every file except `Solution.lean` fixed. Replace its proof hole with a proof
of `BFSTreeSupport.solve`; definitions in `Solution.lean` must stay identical to
`Challenge.lean`. The configuration compares this statement against
the trusted challenge and permits only `propext`, `Quot.sound`, and
`Classical.choice`. An unfilled candidate must fail the axiom check for `sorryAx`.

`verifier.toml` pins Comparator and lean4export. Follow the
[upstream installation and sandbox instructions](https://github.com/leanprover/comparator/tree/d03acab154d269c06e60e4de7e4cc85deebff94b).
On a supported Linux sandbox with those pinned tools installed, run:

```sh
systemd-run --user --wait --pipe --collect \
  --property=RestrictAddressFamilies=~AF_UNIX -E PATH="$PATH" \
  --working-directory="$PWD" -- \
  lake env /path/to/comparator/.lake/build/bin/comparator comparator.json
```

Comparator certification and an independent external kernel check have not been
run for this open template. They cannot certify an unfilled solution. Human
review must still establish that these fixed definitions express the intended
question.

## Semantic evidence

`Tests.lean` checks representative legal and illegal profiles, FIFO violations,
tree simplicity/connectivity, Horn restrictions, empty formulas/clauses and
alternate assignments. From the research repository root, the independent
prepared Python/Z3 oracle can be compared against the Lean predicates with:

```sh
uv sync --locked
uv run --locked python campaigns/bfs-tree-support/work/check.py --self-test
uv run --locked python campaigns/bfs-tree-support/formal/check_semantics.py
```

These are finite semantic checks, not a proof of agreement for all inputs or
evidence that the requested polynomial reduction exists. The independent
campaign and corpus are not needed to use the standalone challenge package.

The source definition follows the fixed board record and campaign contract.
The FIFO reading is consistent with [Rong, Li and Yang, Section 2.2](https://arxiv.org/html/2605.04701v1#S2.SS2).
This addition makes no new literature or novelty claim.
