(set-option :produce-models true)
(set-logic QF_LIA)
(declare-const v0 Int)
(declare-const v1 Int)
(declare-const v2 Int)
(declare-const v3 Int)
(declare-const v4 Int)
(declare-const v5 Int)
(declare-const v6 Int)
(declare-const v7 Int)
(declare-const v8 Int)
(declare-const v9 Int)
(declare-const v10 Int)
(declare-const v11 Int)
(declare-const v12 Int)
(declare-const v13 Int)
(declare-const v14 Int)
(declare-const v15 Int)
(assert (= v0 0))
(assert (or(= v1 (mod (+ v0 1) 16))(= v4 (mod (+ v0 1) 16))))
(assert (or(= v0 (mod (+ v1 1) 16))(= v2 (mod (+ v1 1) 16))(= v5 (mod (+ v1 1) 16))))
(assert (or(= v1 (mod (+ v2 1) 16))(= v3 (mod (+ v2 1) 16))(= v6 (mod (+ v2 1) 16))))
(assert (or(= v2 (mod (+ v3 1) 16))(= v7 (mod (+ v3 1) 16))))
(assert (or(= v0 (mod (+ v4 1) 16))(= v5 (mod (+ v4 1) 16))(= v8 (mod (+ v4 1) 16))))
(assert (or(= v1 (mod (+ v5 1) 16))(= v4 (mod (+ v5 1) 16))(= v6 (mod (+ v5 1) 16))(= v9 (mod (+ v5 1) 16))))
(assert (or(= v2 (mod (+ v6 1) 16))(= v5 (mod (+ v6 1) 16))(= v7 (mod (+ v6 1) 16))(= v10 (mod (+ v6 1) 16))))
(assert (or(= v3 (mod (+ v7 1) 16))(= v6 (mod (+ v7 1) 16))(= v11 (mod (+ v7 1) 16))))
(assert (or(= v4 (mod (+ v8 1) 16))(= v9 (mod (+ v8 1) 16))(= v12 (mod (+ v8 1) 16))))
(assert (or(= v5 (mod (+ v9 1) 16))(= v8 (mod (+ v9 1) 16))(= v10 (mod (+ v9 1) 16))(= v13 (mod (+ v9 1) 16))))
(assert (or(= v6 (mod (+ v10 1) 16))(= v9 (mod (+ v10 1) 16))(= v11 (mod (+ v10 1) 16))(= v14 (mod (+ v10 1) 16))))
(assert (or(= v7 (mod (+ v11 1) 16))(= v10 (mod (+ v11 1) 16))(= v15 (mod (+ v11 1) 16))))
(assert (or(= v8 (mod (+ v12 1) 16))(= v13 (mod (+ v12 1) 16))))
(assert (or(= v9 (mod (+ v13 1) 16))(= v12 (mod (+ v13 1) 16))(= v14 (mod (+ v13 1) 16))))
(assert (or(= v10 (mod (+ v14 1) 16))(= v13 (mod (+ v14 1) 16))(= v15 (mod (+ v14 1) 16))))
(assert (or(= v11 (mod (+ v15 1) 16))(= v14 (mod (+ v15 1) 16))))
(check-sat)
(get-model)