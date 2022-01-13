# profile/classify all used problems between 0 and 100 (0 fastest/easiest, 100 slowest/hardest)
# classification process: we assume 100 is equivalent to 1.5 seconds (all problems with longer runtimes are also
# classified with 100). The other classifications are calculated as round((runtime / 1.5) * 100). The runtimes are
# measured on an Acer Swift 3 Intel Core i5, 8GB RAM
import os.path

problems = {
    "complex": 27,
    "simple1": 2,
    "simple2": 1,
    "simple3": 2,
    # simple set:
    "1_1.smt2": 8,
    "b161test0003.smt2": 2,
    "contraposition-1.smt2": 3,
    "swap_invalid_t3_np_nf_ai_00010_007.cvc.smt2": 4,
    "cpachecker-induction.32_7a_cilled_true-unreach-call_linux-3.8-rc1-drivers--regulator--isl6271a-regulator.ko-main.cil.out.c.smt2": 15,
    "slent_kaluza_201_sink.smt2": 3,
    "R509-011__higher_order_proof__why_c5e835_sparkmnhigher_ordermnfold-T-defqtvc__00.smt2": 8,
    "refcount38.smt2": 3,
    "storeinv_invalid_t3_pp_sf_ai_00004_001.cvc.smt2": 3,
    "double_req_bl_0330a_true-unreach-call.c_2.smt2": 13,
    "float_req_bl_0877_true-unreach-call.c_0.smt2": 3,
    "RND_3_5.smt2": 2,
    "javafe.ast.FieldDecl.149.smt2": 25,
    "swap_invalid_t1_np_nf_ai_00004_002.cvc.smt2": 2,
    # medium set:
    "099-incremental_scheduling-15631-0.smt2": 54,
    "cruise-control.nosummaries.smt2": 38,
    "RND_6_39.smt2": 36,
    "mutex1.smt2": 37,
    "javafe.ast.OnDemandImportDecl.275.smt2": 49,
    "qlock.induction.7.smt2": 46,
    "182.smt2": 60,
    # hard set:
    "151_gcc.smt2": 98,
    "splice_true-unreach-call_false-valid-memtrack.i_10.smt2": 85,
    "javafe.ast.ArrayRefExpr.40.smt2": 100,
    "egcd3-ll_valuebound50-O0.smt2": 99,
    "bresenham-ll_valuebound2-O0.smt2": 90,
    "orb05_700.smt2": 100,
    "digital-stopwatch.locals.smt2": 95,
    "s3_srvr.blast.01_false-unreach-call.i.cil.c_0.smt2": 98,
    "183.smt2": 67,
    # training set:
    "2_1.smt2": 1,
    "small-dyn-partition-fixpoint-4.smt2": 1,
    "agree3.smt2": 1,
    "intersection-example-simple.proof-node3202.smt2": 1,
    "read8.smt2": 1,
    "storecomm_invalid_t1_np_nf_ai_00060_006.cvc.smt2": 1,
    "nested9_true-unreach-call.i_7.smt2": 1,
    "adacore_u__communication.adb_40_34_range_check___00.smt2": 1,
    "adacore_u__p_max_array.ads_18_48_overflow_check___00.smt2": 1
    # there are some duplicates defined already in other sets
}


def get_problem_complexity(smt_problem):
    return problems.get(os.path.basename(smt_problem), 100)
