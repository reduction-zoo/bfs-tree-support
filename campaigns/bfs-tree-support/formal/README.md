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

Lean 4.35.0 and Mathlib tag `v4.35.0` (commit
`56a005855ea17e0b0958f73ec801ae140b0a1679`) are pinned by `lean-toolchain`,
`lakefile.toml` and `lake-manifest.json`. In this directory:

```sh
lake exe cache get Mathlib.Computability.TuringMachine.Computable
LEAN_NUM_THREADS=2 lake build
lake env lean Audit.lean
```

The cache download requires network access on a fresh checkout; it can be
omitted when the pinned dependencies and Mathlib cache are already present.
`lake build` includes `Tests.lean`. The entry files use `module`, `public import`
and `public section`; all problem definitions remain inlined in each file.

Only the two open theorem placeholders should report `sorry`. The definitions
and `Goal` have no proof holes. Compilation and semantic tests establish a
well-formed specification, not a solution of the open question.

## Submit a solution to Comparator

Keep every file except `Solution.lean` fixed. Replace its proof hole with a proof
of `BFSTreeSupport.solve`; definitions in `Solution.lean` must stay identical to
`Challenge.lean`. The configuration compares this statement against
the trusted challenge and permits only `propext`, `Quot.sound`, and
`Classical.choice`. An unfilled candidate must fail the axiom check for `sorryAx`.

Lean 4.35.0 bundles `lake comparator`, its exporter, Lean's kernel checker and
the independent NanoDa and con-ron kernels. No separate comparator checkout is
needed. On Linux with `bubblewrap` (`bwrap`) installed, from this directory:

```sh
lake comparator --config comparator.json
./scripts/verify-comparator.sh
```

The first command uses the unchanged strict axiom policy and must reject the
unfilled solution with `error: Illegal axiom detected: 'sorryAx'`. Comparator
checks the statement and its definitions before checking axioms.

The script adapts [PalomarTemplate](https://github.com/PalomarRegistry/PalomarTemplate)'s
verification with both bundled independent kernels enabled. It accepts either:

- A completed solution accepted under the strict policy, including kernel replay.
- The exact `sorryAx` rejection (exit 1), followed by full comparator acceptance
  with **only** `sorryAx` temporarily added to a generated config. This second
  pass rules out additional forbidden axioms and requires all three kernels to
  accept. It verifies the open template, **not a proof**. `comparator.json` is
  never relaxed or modified.

Every other failure fails CI. The repo-root [Lean workflow](../../../.github/workflows/lean.yml)
builds this subdirectory (including `Tests.lean`), audits `Goal`, tests the
script on real small Lake projects, then runs it on this question. Thus green
CI for the unfilled copy means a correctly posed open question; after a proof
is filled in, strict comparator acceptance is required without a workflow edit.
The script can be invoked from any working directory and uses the project's
pinned toolchain. It does not download the Mathlib cache itself.

macOS cannot run the required Linux namespace sandbox. The local build, audit
and finite semantic evidence are in `evidence/statement/*.log`; sandboxed
comparator and independent kernel verification await Linux CI. Human review
must still establish that the definitions express the intended question.

## Metadata and licensing

`formalization.yaml` follows PalomarTemplate's v0.4 metadata shape and records
the open statement, the unfilled solution and git authorship. This repository
has **no LICENSE file** and no declared repository licence. The metadata says
`unknown`; it does not grant Apache-2.0 or any other licence. An authorized
licence decision and a LICENSE file are needed before a licensed Palomar
submission; the template's Apache-only licence validator would reject this state.

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
