"""Compare the Lean specification with the independent prepared source/Z3 oracles."""
from itertools import product
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent / "work"
sys.path.insert(0, str(WORK))
from check import bfs_order_possible, is_tree, legal_target, tree_edges, valid_target


def lean(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "[" + ", ".join(map(lean, value)) + "]"
    return str(value)


lines = ["import Definitions", "open BFSTreeSupport"]
source_queries = 0
cases = json.loads((WORK / "cases.json").read_text())
for case in cases:
    orders = case["source"]["orders"]
    n = len(orders[0])
    profile = f"⟨{n}, {lean(orders)}⟩"
    for sequence in product(range(n), repeat=max(0, n - 2)):
        edges = tree_edges(sequence, n)
        expected = is_tree(n, edges) and all(bfs_order_possible(n, edges, order) for order in orders)
        tree = "[" + ", ".join(f"({u}, {v})" for u, v in edges) + "]"
        lines.append(f"#guard supports {profile} {tree} == {lean(expected)}")
        source_queries += 1

target_queries = 0
formula_count = 0
for n in range(4):
    literals = [lit for v in range(1, n + 1) for lit in (v, -v)]
    clauses = [[]] + [[lit] for lit in literals]
    clauses += [[a, b] for a in literals for b in literals
                if a < b and sum(x > 0 for x in (a, b)) <= 1]
    for first in clauses:
        for second in clauses:
            target = {"num_vars": n, "clauses": [first, second]}
            assert legal_target(target)
            encoded = "[" + ", ".join(
                "[" + ", ".join(f"⟨{abs(lit) - 1}, {lean(lit > 0)}⟩" for lit in clause) + "]"
                for clause in target["clauses"]) + "]"
            for assignment in product((False, True), repeat=n):
                values = list(assignment)
                expected = valid_target(target, {"assignment": values})
                lines.append(f"#guard satisfies ⟨{n}, {encoded}⟩ {lean(values)} == {lean(expected)}")
                target_queries += 1
            formula_count += 1

generated = ROOT / ".lake/OracleChecks.lean"
generated.write_text("\n".join(lines) + "\n")
subprocess.run(["lake", "env", "lean", str(generated)], cwd=ROOT, check=True)
print(f"Lean agrees with independent oracles: {len(cases)} profiles, {source_queries} tree checks; "
      f"{formula_count} Horn formulas, {target_queries} assignment checks.")
