# BFS tree support → Horn satisfiability

Independent research campaign for the [fixed question](campaigns/bfs-tree-support/question.md). [State](campaigns/bfs-tree-support/state.md) records the current evidence and next action.

The initial commit fixes the question and setup. [Prepare evidence](campaigns/bfs-tree-support/work/preparation.md), [contract](campaigns/bfs-tree-support/work/contract.md), and [fixed corpus](campaigns/bfs-tree-support/work/cases.json) are committed. No solution is claimed. Run the campaign from this repository and follow `AGENTS.md`.

Reproduce: `uv sync --locked`, then `uv run --locked python campaigns/bfs-tree-support/work/check.py --self-test`.

The [standalone Lean definition and Comparator challenge](campaigns/bfs-tree-support/formal/README.md)
fix the source/target semantics and polynomial-time reduction goal. This is a
formal statement of the open question, not a solution.
