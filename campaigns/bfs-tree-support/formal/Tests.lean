import Challenge

open BFSTreeSupport

#guard legalProfile ⟨1, [[0]]⟩
#guard !legalProfile ⟨0, [[]]⟩
#guard !legalProfile ⟨2, [[0, 0]]⟩
#guard !legalProfile ⟨2, []⟩
#guard supports ⟨1, [[0]]⟩ []
#guard supports ⟨3, [[0, 1, 2], [1, 0, 2]]⟩ [(0, 1), (0, 2)]
#guard !supports ⟨4, [[0, 1, 3, 2]]⟩ [(0, 1), (0, 2), (1, 3)]
-- Same BFS levels are insufficient: FIFO must finish the first parent's children first.
#guard !supports ⟨5, [[0, 1, 2, 4, 3]]⟩ [(0, 1), (0, 2), (1, 3), (2, 4)]
#guard !supports ⟨3, [[0, 1, 2]]⟩ [(0, 1), (1, 0)]
#guard !supports ⟨3, [[0, 1, 2]]⟩ [(0, 1), (1, 2), (2, 0)]
#guard !isTree 4 [(0, 1), (1, 2), (2, 0)]
#guard legalHorn ⟨0, []⟩
#guard satisfies ⟨0, []⟩ []
#guard !satisfies ⟨0, [[]]⟩ []
#guard !legalHorn ⟨2, [[⟨0, true⟩, ⟨1, true⟩]]⟩
#guard !legalHorn ⟨1, [[⟨0, true⟩, ⟨0, true⟩]]⟩
#guard !legalHorn ⟨1, [[⟨1, false⟩]]⟩
#guard !satisfies ⟨2, [[⟨0, true⟩]]⟩ [true]
#guard satisfies ⟨2, [[⟨0, true⟩], [⟨0, false⟩, ⟨1, true⟩]]⟩ [true, true]
#guard !satisfies ⟨2, [[⟨0, true⟩], [⟨0, false⟩, ⟨1, true⟩]]⟩ [true, false]
#guard (encodeNat (2 ^ 20)).length == 43

example : ¬validSourceOutput ⟨1, [[0]]⟩ none := by
  intro h
  exact h.2 ⟨[], by decide⟩

example : validTargetOutput ⟨0, [[]]⟩ none := by
  constructor
  · decide
  · rintro ⟨assignment, h⟩
    simp [satisfies, legalHorn] at h
