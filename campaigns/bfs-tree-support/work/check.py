"""Independent tree-support and Horn-SAT oracles."""

import argparse
import json
import subprocess
import sys
from collections import deque
from itertools import product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict) or not isinstance(source.get("orders"), list) or not source["orders"]:
        return False
    orders = source["orders"]
    if not isinstance(orders[0], list):
        return False
    n = len(orders[0])
    return n >= 1 and all(isinstance(order, list) and len(order) == n
                          and all(type(v) is int for v in order)
                          and set(order) == set(range(n)) for order in orders)


def tree_edges(sequence, n):
    if n == 1:
        return []
    degrees = [1] * n
    for v in sequence:
        degrees[v] += 1
    edges = []
    for v in sequence:
        leaf = next(i for i in range(n) if degrees[i] == 1)
        edges.append([leaf, v])
        degrees[leaf] -= 1
        degrees[v] -= 1
    ends = [i for i in range(n) if degrees[i] == 1]
    edges.append(ends)
    return edges


def is_tree(n, edges):
    if not isinstance(edges, list) or len(edges) != n - 1:
        return False
    neighbors = [set() for _ in range(n)]
    for edge in edges:
        if (not isinstance(edge, list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1] or edge[1] in neighbors[edge[0]]):
            return False
        u, v = edge
        neighbors[u].add(v)
        neighbors[v].add(u)
    seen, queue = {0}, deque([0])
    while queue:
        for neighbor in neighbors[queue.popleft()]:
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return len(seen) == n


def bfs_order_possible(n, edges, order):
    neighbors = [set() for _ in range(n)]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    seen, queue, position = {order[0]}, deque([order[0]]), 1
    while queue:
        u = queue.popleft()
        new = neighbors[u] - seen
        batch = order[position:position + len(new)]
        if set(batch) != new:
            return False
        seen.update(batch)
        queue.extend(batch)
        position += len(new)
    return position == n


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    edges = output.get("edges")
    n = len(source["orders"][0])
    return (set(output) == {"edges"} and is_tree(n, edges)
            and all(bfs_order_possible(n, edges, order) for order in source["orders"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal BFS profile")
    n = len(source["orders"][0])
    for sequence in product(range(n), repeat=max(0, n-2)):
        edges = tree_edges(sequence, n)
        if all(bfs_order_possible(n, edges, order) for order in source["orders"]):
            return {"edges": edges}
    return {"status": "NO-SOLUTION"}


def legal_target(target):
    if not isinstance(target, dict):
        return False
    n, clauses = target.get("num_vars"), target.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list)
                    and all(type(lit) is int and 1 <= abs(lit) <= n for lit in clause)
                    and sum(lit > 0 for lit in clause) <= 1
                    for clause in clauses))


def target_solutions(target, limit=3):
    if not legal_target(target):
        raise ValueError("Illegal Horn formula")
    variables = [z3.Bool(f"h{i}") for i in range(target["num_vars"])]
    solver = z3.Solver()
    for clause in target["clauses"]:
        solver.add(z3.Or(*(variables[abs(lit)-1] if lit > 0
                           else z3.Not(variables[-lit-1]) for lit in clause)))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive Horn solver: {result}")
        model = solver.model()
        assignment = [z3.is_true(model.eval(v, model_completion=True)) for v in variables]
        outputs.append({"assignment": assignment})
        solver.add(z3.Or(*[v != value for v, value in zip(variables, assignment)]))
    return outputs or [{"status": "NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target, 1)[0]


def valid_target(target, output):
    if not legal_target(target) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_target(target) == output
    assignment = output.get("assignment")
    return (set(output) == {"assignment"} and isinstance(assignment, list)
            and len(assignment) == target["num_vars"]
            and all(type(value) is bool for value in assignment)
            and all(any(assignment[abs(lit)-1] == (lit > 0) for lit in clause)
                    for clause in target["clauses"]))


def exhaustive_target(target):
    for bits in product((False, True), repeat=target["num_vars"]):
        output = {"assignment": list(bits)}
        if all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
               for clause in target["clauses"]):
            return output
    return {"status": "NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES, random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable, str(root / "research/validate_preparation.py"), str(path)], check=True, cwd=root)
    cases = json.loads(path.read_text())
    for orders, expected in EDGE_CASES:
        assert ("edges" in solve_source({"orders": orders})) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("edges" in current) == ("edges" in case["expected"])
        assert valid_source(source, current) and valid_source(source, case["expected"])
    test_hand_cases()
    checked = 0
    for n in range(4):
        literals = [lit for v in range(1, n+1) for lit in (v, -v)]
        clauses = [[]] + [[lit] for lit in literals]
        clauses += [[a, b] for a in literals for b in literals if a < b and sum(x > 0 for x in (a,b)) <= 1]
        for first in clauses:
            for second in clauses:
                target = {"num_vars": n, "clauses": [first, second]}
                assert ("assignment" in solve_target(target)) == ("assignment" in exhaustive_target(target))
                checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive Horn formulas")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable, str(path)], input=json.dumps(source), text=True, capture_output=True, check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal Horn target: {target}")
        for output in target_solutions(target):
            if not valid_target(target, output):
                raise AssertionError(f"Target oracle returned invalid output: {output}")
            payload = {"source": source, "target_solution": output}
            extraction = subprocess.run([sys.executable, str(path), "--extract"], input=json.dumps(payload), text=True, capture_output=True, check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source, recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test", action="store_true")
    group.add_argument("--candidate", type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
