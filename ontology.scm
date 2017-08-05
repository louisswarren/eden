(set! COMMENT-FLAG #f)
(libload "nat.scm")
(libload "list.scm")
(set! COMMENT-FLAG #t)

(add-algs "formula"
  '("Atomic" "nat=>formula")
  '("Implication" "formula=>formula=>formula")) (add-var-name "a" "b" "c" (py "formula"))
(add-infix-display-string "Implication" "implies" 'pair-op)

(add-algs "deduction"
  '("Assumption" "formula=>deduction")
  '("ImplicationElim" "deduction=>deduction=>deduction")
  '("ImplicationIntro" "deduction=>formula=>deduction"))
(add-var-name "dd" "de" "df" (py "deduction"))


(add-program-constant "ImplicationPremise" (py "formula=>formula"))
(add-computation-rule "ImplicationPremise (Implication a b)" "a")

(add-program-constant "ImplicationConclusion" (py "formula=>formula"))
(add-computation-rule "ImplicationConclusion (Implication a b)" "b")


(add-program-constant "Result" (py "deduction=>formula"))
(add-computation-rules
  "Result (Assumption a)" "a"
  "Result (ImplicationElim dd de)"
    "[if ((ImplicationPremise (Result dd)) = (Result de))
        (ImplicationConclusion (Result dd))
        (Result dd)]"
  "Result (ImplicationIntro dd a)" "Implication a (Result dd)")

(add-program-constant "OpenAssumptions" (py "deduction=>list formula"))
(add-computation-rules
  "OpenAssumptions (Assumption a)" "a:"
  "OpenAssumptions (ImplicationElim dd de)" 


(add-program-constant "P" (py "formula"))
(add-program-constant "Q" (py "formula"))
(add-program-constant "R" (py "formula"))
(add-computation-rules
  "P" "Atomic 0"
  "Q" "Atomic 1"
  "R" "Atomic 2")

(set-goal "Result (
  ImplicationElim
    (Assumption (P implies (P implies Q)))
    (Assumption P)
)")
(ng)



(set-goal "ListFilter P :: Q :: R:")
(ng)
