problems = {
    "simple1": 1,
    "simple2": 2,
    "simple3": 3,
    "latency_evaluation/refcount38.smt2": 5,
    "complex": 50
}  # TODO: profile/classify all used problems between 1 and 100 (1 fastest, 100 slowest)


def get_problem_complexity(smt_problem):
    return problems.get(smt_problem, 100)
