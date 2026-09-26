# BFS tree support → Horn satisfiability

Category: Complexity open

## Source

The source gives an explicit nonempty list of permutations of the same n vertices, n≥1. Its output is a tree realizing all orders as FIFO breadth-first traversals, with arbitrary neighbor tie orders, or NO-SOLUTION.

## Target

An explicitly listed nonempty profile of permutations must be realized by FIFO breadth-first search on one tree, with arbitrary neighbor tie orders. The target is an explicit Horn formula; its outputs are satisfying assignments or NO-SOLUTION.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

A polynomial reduction would give both recognition and tree construction for the remaining traversal-support case.

## Difficulty

The exact parent compatibility representation is available, but neither propagation completeness nor extraction is proved. Greedy and contraction routes have counterexamples.

## Literature context

Published traversal-support classifications leave the BFS case open; the polynomial algorithms for DFS and general search do not imply FIFO consistency.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [arXiv:2605.04701v1](https://arxiv.org/html/2605.04701v1): Rong, Li and Yang, *When Graph Traversal Meets Structured Preferences: Unified Framework and Complexity Results*, arXiv:2605.04701v1, 6 May 2026, https://arxiv.org/html/2605.04701v1, Sections 1.2, 2.2 and 4.1, explicitly leaves BFS tree-support recognition open. BFS and LexBFS coincide on trees. Their DFS algorithm and GS attachment representation do not establish the BFS result. Section 4.1 Algorithm 1 intersects blockers; the union symbol in the preceding prose is inconsistent with that algorithm and is not used here.

Fixed from board record `website/questions/bfs-tree-support.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
