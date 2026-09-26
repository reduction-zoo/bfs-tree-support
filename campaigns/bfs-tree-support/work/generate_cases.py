"""Fix reproducible BFS tree-support profiles before construction."""

import json
import random
from collections import deque
from pathlib import Path


EDGE_CASES = [
    ([[0]], True),
    ([[0, 1]], True), ([[1, 0]], True), ([[0, 1], [1, 0]], True),
    ([[0, 1, 2]], True), ([[0, 2, 1]], True),
    ([[1, 0, 2]], True), ([[1, 2, 0]], True),
    ([[2, 0, 1]], True), ([[2, 1, 0]], True),
    ([[0, 1, 2], [0, 2, 1]], True),
    ([[0, 1, 2], [0, 2, 1], [1, 2, 0]], False),
    ([[0, 1, 2, 3]], True),
]


def star_bfs(n, center, root, rng):
    neighbors = [[center] if v != center else [u for u in range(n) if u != center]
                 for v in range(n)]
    for row in neighbors:
        rng.shuffle(row)
    order, queue, seen = [], deque([root]), {root}
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in neighbors[u]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return order


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(3, 5)
    count = rng.randint(2, 4)
    if seed % 2 == 0:
        center = rng.randrange(n)
        orders = [star_bfs(n, center, rng.randrange(n), rng) for _ in range(count)]
    else:
        orders = [rng.sample(range(n), n) for _ in range(count)]
    return {"orders": orders}


def build_cases():
    from check import solve_source

    cases, seen = [], set()

    def add(source, kind, seed=None, hand_answer=None):
        key = json.dumps(source, sort_keys=True, separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("edges" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source": source, "kind": kind, "expected": answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for orders, answer in EDGE_CASES:
        add({"orders": orders}, "edge", hand_answer=answer)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed), "random", seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases, indent=2) + "\n")
    print(f"Wrote {len(cases)} cases to {path}")
