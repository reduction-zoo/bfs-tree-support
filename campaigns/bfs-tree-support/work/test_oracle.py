from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    single = {"orders": [[0]]}
    assert solve_source(single) == {"edges": []}
    assert valid_source(single, {"edges": []})
    impossible = {"orders": [[0, 1, 2], [0, 2, 1], [1, 2, 0]]}
    assert solve_source(impossible) == {"status": "NO-SOLUTION"}
    assert not valid_source(single, {"status": "NO-SOLUTION"})
    assert not legal_source({"orders": [[0, 0]]})
    horn = {"num_vars": 2, "clauses": [[1], [-1, 2], [-2]]}
    assert solve_target(horn) == {"status": "NO-SOLUTION"}
    assert not valid_target(horn, {"assignment": [True, True]})
    assert not legal_target({"num_vars": 2, "clauses": [[1, 2]]})


if __name__ == "__main__":
    test_hand_cases()
