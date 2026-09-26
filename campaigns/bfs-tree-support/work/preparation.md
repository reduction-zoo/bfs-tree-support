# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus has 113 distinct
legal BFS profiles: 13 hand-labelled edge cases and 100 seeded random cases.
There are 92 YES and 21 NO cases, with one to five vertices and one to four
orders per profile. The generator makes some positive profiles by running BFS
on a star with random roots and tie orders; other profiles are independently
random. The seeds and expected outputs are retained in `generate_cases.py`
and `cases.json`.

The source oracle enumerates labelled trees via Prüfer sequences over this
finite domain. For a fixed tree and requested BFS order, a direct FIFO queue
test checks that each vertex's undiscovered neighbors equal the next batch in
the order. This condition is necessary and sufficient because that batch can
be chosen as the vertex's neighbor tie order. The returned tree is validated
for edge count, simplicity, connectivity and every requested traversal.
Exhausting the trees establishes NO-SOLUTION for the finite instances. The
hand labels include the one-vertex tree, all one-order three-vertex profiles,
compatible tie orders and an incompatible three-order profile.

The Horn target oracle uses Z3 4.16.0: each clause is an exact Boolean
disjunction. SAT models are checked by direct clause evaluation; UNSAT is
conclusive and unknown is an error. Exhaustive Boolean assignments agreed
with Z3 on 478 Horn formulas with zero to three variables, including empty
clauses. Hand fixtures reject a non-Horn clause, an invalid assignment and a
false positive satisfiability claim.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/bfs-tree-support/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates all random profiles,
rechecks each source answer, and compares target decisions to exhaustive
enumeration. The candidate runner uses separate forward and recovery
subprocesses and up to three Horn assignments per case. An incorrect injected
candidate was rejected after its Horn target was solved and its recovered
NO-SOLUTION was directly invalidated. No actual reduction candidate exists.
The finite tests do not establish a polynomial reduction or settle this
recognition question.
