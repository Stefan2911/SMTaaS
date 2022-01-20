# 1. execute all problems on the robot and on the RPi's
# 2. define upper bound execution time for robot and RPi's
# 3. calculate classification with round((runtime / upper_bound_execution_time) * 100)
# 4. the higher the harder, the lower the easier
import os.path

problems = {
    "complex": 24, "simple1": 1, "simple2": 1, "simple3": 2,
    # simple set:
    "1_1.smt2": 3,
    "b161test0003.smt2": 2,
    "contraposition-1.smt2": 3,
    "cpachecker-induction.32_7a_cilled_true-unreach-call_linux-3.8-rc1-drivers--regulator--isl6271a-regulator.ko-main.cil.out.c.smt2": 15,
    "double_req_bl_0330a_true-unreach-call.c_2.smt2": 3,
    "float_req_bl_0877_true-unreach-call.c_0.smt2": 2,
    "javafe.ast.FieldDecl.149.smt2": 27,
    "R509-011__higher_order_proof__why_c5e835_sparkmnhigher_ordermnfold-T-defqtvc__00.smt2": 5,
    "refcount38.smt2": 4,
    "RND_3_5.smt2": 2,
    "slent_kaluza_201_sink.smt2": 3,
    "storeinv_invalid_t3_pp_sf_ai_00004_001.cvc.smt2": 2,
    "swap_invalid_t1_np_nf_ai_00004_002.cvc.smt2": 19,
    "swap_invalid_t3_np_nf_ai_00010_007.cvc.smt2": 3,
    # medium set:
    "cruise-control.nosummaries.smt2": 21,
    "mutex1.smt2": 38,
    "099-incremental_scheduling-15631-0.smt2:": 30,
    "javafe.ast.OnDemandImportDecl.275.smt2": 45,
    "182.smt2": 37,
    "RND_6_39.smt2": 32,
    "qlock.induction.7.smt2": 49,
    # hard set:
    "151_gcc.smt2": 120,
    "egcd3-ll_valuebound50-O0.smt2": 101,
    "splice_true-unreach-call_false-valid-memtrack.i_10.smt2": 47,
    "s3_srvr.blast.01_false-unreach-call.i.cil.c_0.smt2": 89,
    "bresenham-ll_valuebound2-O0.smt2": 96,
    "orb05_700.smt2": 27,
    "digital-stopwatch.locals.smt2": 101,
    "javafe.ast.ArrayRefExpr.40.smt2": 96,
    "183.smt2": 37,
    # training set:
    "agree3.smt2": 3,
    "intersection-example-simple.proof-node3202.smt2": 2,
    "nested9_true-unreach-call.i_7.smt2": 2,
    "2_1.smt2": 3,
    # there are some duplicates defined already in other sets
}

problems_ev3 = {
    "complex": 892, "simple1": 7, "simple2": 7, "simple3": 50,
    # simple set:
    "1_1.smt2": 40,
    "b161test0003.smt2": 25,
    "contraposition-1.smt2": 61,
    "cpachecker-induction.32_7a_cilled_true-unreach-call_linux-3.8-rc1-drivers--regulator--isl6271a-regulator.ko-main.cil.out.c.smt2": 569,
    "double_req_bl_0330a_true-unreach-call.c_2.smt2": 20,
    "float_req_bl_0877_true-unreach-call.c_0.smt2": 19,
    "javafe.ast.FieldDecl.149.smt2": 1042,
    "R509-011__higher_order_proof__why_c5e835_sparkmnhigher_ordermnfold-T-defqtvc__00.smt2": 132,
    "refcount38.smt2": 31,
    "RND_3_5.smt2": 12,
    "slent_kaluza_201_sink.smt2": 63,
    "storeinv_invalid_t3_pp_sf_ai_00004_001.cvc.smt2": 33,
    "swap_invalid_t1_np_nf_ai_00004_002.cvc.smt2": 70,
    "swap_invalid_t3_np_nf_ai_00010_007.cvc.smt2": 77,
    # medium set:
    "cruise-control.nosummaries.smt2": 1150,
    "mutex1.smt2": 1754,
    "099-incremental_scheduling-15631-0.smt2": 1729,
    "javafe.ast.OnDemandImportDecl.275.smt2": 1944,
    "182.smt2": 1513,
    "RND_6_39.smt2": 1326,
    "qlock.induction.7.smt2": 1707,
    # hard set:
    "151_gcc.smt2": 4490,
    "egcd3-ll_valuebound50-O0.smt2": 3973,
    "splice_true-unreach-call_false-valid-memtrack.i_10.smt2": 1737,
    "s3_srvr.blast.01_false-unreach-call.i.cil.c_0.smt2": 3645,
    "bresenham-ll_valuebound2-O0.smt2": 3912,
    "orb05_700.smt2": 3502,
    "digital-stopwatch.locals.smt2": 3905,
    "javafe.ast.ArrayRefExpr.40.smt2": 4829,
    "183.smt2": 1510,
    # training set:
    "agree3.smt2": 71,
    "intersection-example-simple.proof-node3202.smt2": 38,
    "nested9_true-unreach-call.i_7.smt2": 32,
    "2_1.smt2": 82,
    # there are some duplicates defined already in other sets
}


def get_problem_complexity(smt_problem, is_ev3):
    name = os.path.basename(smt_problem)
    if is_ev3:
        return problems_ev3.get(name, 100)
    return problems.get(os.path.basename(smt_problem), 100)
