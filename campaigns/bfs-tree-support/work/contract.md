# Prepared input and output contract

The source input is `{"orders": [[vertex, ...], ...]}`: a nonempty list of
permutations of `0..n-1` for one `n >= 1`. A source output is
`{"edges": [[u, v], ...]}`, a simple undirected tree on those vertices for
which every given order is a possible FIFO breadth-first traversal, each
allowed its own arbitrary neighbor tie order. `{"status": "NO-SOLUTION"}`
is valid exactly when no tree realizes the full profile.

The Horn target input is `{"num_vars": n, "clauses": [[signed_literals],
...]}` with `n >= 0`, each nonzero literal in range `1..n`, and at most one
positive literal per clause. Empty clauses and repeated literals are legal.
A target output is `{"assignment": [bool, ...]}` satisfying all clauses, or
`{"status": "NO-SOLUTION"}` exactly when unsatisfiable.

A candidate `algorithm.py` reads a source JSON object from stdin and writes a
legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors, and write
diagnostics to stderr. They must be deterministic and polynomial time, and
recovery must work for every valid Horn output, including alternate
assignments and NO-SOLUTION.

`check.py --candidate PATH` injects the fixed source corpus, solves each Horn
target independently, and directly checks each recovered tree or negative
decision.
