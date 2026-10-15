/-
Challenge.lean: the trusted Comparator statement of board question Q001,
BFS tree support → Horn satisfiability.

This file is standalone. It imports only Mathlib and fixes the two problems,
their finite binary encodings, NO-SOLUTION semantics and the exact reduction
goal. The theorem `BFSTreeSupport.solve` states the open question; its `sorry`
is deliberate. Comparator accepts `Solution.lean` only if it proves this
theorem with the identical statement and identical definitions, using only the
axioms propext, Quot.sound and Classical.choice.
-/
import Mathlib.Computability.TuringMachine.Computable

/-! The fixed problem, not a proposed reduction. Vertex and variable indices are
zero-based. Every object has an explicit finite binary encoding below. -/

namespace BFSTreeSupport

structure Profile where
  numVertices : Nat
  orders : List (List Nat)
  deriving Repr

abbrev Tree := List (Nat × Nat)

/-- Nonempty profiles of permutations of precisely the admitted vertices. -/
def legalProfile (x : Profile) : Bool :=
  x.numVertices > 0 && !x.orders.isEmpty &&
    x.orders.all (fun order => decide (order.Perm (List.range x.numVertices)))

def adjacent (edges : Tree) (u v : Nat) : Bool :=
  edges.any (fun e => (e.1 == u && e.2 == v) || (e.1 == v && e.2 == u))

/-- FIFO traversal. Newly discovered neighbors use the requested order as their
tie order. Each legal traversal is reproduced by exactly this choice of ties. -/
def bfsRun (edges : Tree) (tieOrder : List Nat) :
    Nat → List Nat → List Nat → List Nat
  | 0, _, seen => seen
  | _ + 1, [], seen => seen
  | fuel + 1, u :: queue, seen =>
    let children := tieOrder.filter (fun v => adjacent edges u v && !seen.contains v)
    bfsRun edges tieOrder fuel (queue ++ children) (seen ++ children)

def bfs (edges : Tree) (order : List Nat) : List Nat :=
  match order with
  | [] => []
  | root :: _ => bfsRun edges order order.length [root] [root]

/-- A simple connected graph with n−1 edges, hence a tree. Reversing an edge
does not change it; repeated unordered edges and loops are rejected. -/
def isTree (n : Nat) (edges : Tree) : Bool :=
  n > 0 && edges.length == n - 1 &&
    edges.all (fun e => e.1 < n && e.2 < n && e.1 != e.2) &&
    decide ((edges.map (fun e => (min e.1 e.2, max e.1 e.2))).Nodup) &&
    (bfs edges (List.range n)).length == n

/-- Every order may choose its own root and neighbor tie orders on the same tree. -/
def supports (x : Profile) (edges : Tree) : Bool :=
  legalProfile x && isTree x.numVertices edges &&
    x.orders.all (fun order => bfs edges order == order)

/-- None is a mathematical NO-SOLUTION answer, never an execution error. -/
def validSourceOutput (x : Profile) : Option Tree → Prop
  | some edges => supports x edges = true
  | none => legalProfile x = true ∧ ¬ ∃ edges, supports x edges = true

structure Literal where
  index : Nat
  positive : Bool
  deriving Repr

structure Horn where
  numVars : Nat
  clauses : List (List Literal)
  deriving Repr

/-- Empty clauses and repeated literals are admitted. Positive occurrences,
not distinct positive variable names, are counted as in the fixed input contract. -/
def legalHorn (h : Horn) : Bool :=
  h.clauses.all (fun clause =>
    clause.all (fun lit => lit.index < h.numVars) &&
    (clause.filter (fun lit => lit.positive)).length ≤ 1)

def satisfies (h : Horn) (assignment : List Bool) : Bool :=
  legalHorn h && assignment.length == h.numVars &&
    h.clauses.all (fun clause => clause.any (fun lit =>
      assignment[lit.index]? == some lit.positive))

def validTargetOutput (h : Horn) : Option (List Bool) → Prop
  | some assignment => satisfies h assignment = true
  | none => legalHorn h = true ∧ ¬ ∃ assignment, satisfies h assignment = true

/-- A self-delimiting binary natural: unary bit-length, separator, binary digits.
Its length is O(log(n+2)); the natural itself is not represented in unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeProfile (x : Profile) : List Bool :=
  encodeNat x.numVertices ++ encodeList (encodeList encodeNat) x.orders

def encodeTree (edges : Tree) : List Bool :=
  encodeList (fun e => encodeNat e.1 ++ encodeNat e.2) edges

def encodeHorn (h : Horn) : List Bool :=
  encodeNat h.numVars ++ encodeList
    (encodeList (fun lit => encodeNat lit.index ++ [lit.positive])) h.clauses

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

def encodeRecoveryInput (input : Profile × Option (List Bool)) : List Bool :=
  encodeProfile input.1 ++ encodeOption (encodeList (fun b => [b])) input.2

/-- A solution supplies both unknown deterministic algorithms. Their running time
is certified in Mathlib's finite-alphabet stack Turing-machine model, using the
actual binary encodings above. Recovery time is measured on the full pair (x,y). -/
def Reduction (forward : Profile → Horn)
    (recover : Profile × Option (List Bool) → Option Tree) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeProfile encodeHorn forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime encodeRecoveryInput
    (encodeOption encodeTree) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeHorn (forward x)).length ≤ bound.eval (encodeProfile x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    (encodeOption encodeTree (recover input)).length ≤
      bound.eval (encodeRecoveryInput input).length) ∧
  (∀ x, legalProfile x = true → legalHorn (forward x) = true) ∧
  (∀ x, legalProfile x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

/-- The open question: construct a polynomial-time reduction with universal
output recovery. No particular construction or extra source promise is fixed. -/
def Goal : Prop :=
  ∃ (forward : Profile → Horn)
    (recover : Profile × Option (List Bool) → Option Tree), Reduction forward recover

/-- The open question. The placeholder is not a correctness certificate. -/
theorem solve : Goal := by
  sorry

end BFSTreeSupport
