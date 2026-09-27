# Research instructions

Read the [fixed question](campaigns/bfs-tree-support/question.md), [prior state](campaigns/bfs-tree-support/state.md) and [preparation notes](campaigns/bfs-tree-support/work/preparation.md). The fixed [test corpus](campaigns/bfs-tree-support/work/cases.json) and [verifier](campaigns/bfs-tree-support/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/bfs-tree-support/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
