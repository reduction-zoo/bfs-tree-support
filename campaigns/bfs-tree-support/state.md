# BFS tree support → Horn satisfiability campaign state

Status: Prepare completed on 2026-09-26. No reduction or solution is claimed.

Capability probe (2026-09-26): Python 3.12.14, uv 0.12.17, Z3 4.16.0 from the locked environment, Typst 0.15.1, Lake 5.0.0 and Lean 4.34.1 available.

Next action: use the committed corpus, verifier and contract for the next user-directed campaign.

| ID | Attempted mechanism or literature scope | First check | Outcome | Evidence |
|---|---|---|---|---|

## Formal question definition

The [standalone Lean package](formal/README.md) fixes `BFSTreeSupport.Goal`:
polynomial-time construction and recovery with the full (I, S) contract,
including FIFO ties, all valid Horn assignments and NO-SOLUTION. Definitions
compile without proof holes; `Challenge.lean` and `Solution.lean` deliberately
leave the open theorem unproved. The axiom audit of `Goal` reports only the
three permitted foundational axioms. See [build evidence](formal/evidence/statement/build.log)
and [the axiom audit](formal/evidence/statement/axioms.log).

Finite differential checks compare the definitions against the prepared independent
oracles on 113 profiles (4,459 labelled-tree checks) and 478 Horn formulas
(3,321 assignment checks). This does not solve the question or establish universal
implementation agreement. Comparator and an external kernel check remain pending.
