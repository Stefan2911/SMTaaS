(set-logic QF_UF)
(declare-const p Bool)
(assert (and p (not p)))
(check-sat)