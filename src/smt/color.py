from pysmt.shortcuts import And, Solver, Symbol, NotEquals, Equals, Int
from pysmt.typing import INT


def color(V, E, k):
    """
    Attempt to color the graph G(V, E) with k colors
    (or find the chromatic number of G if k=None)
    Returns:
    * The assignment of vertices --> colors, if satisfiable
    * False, if not satisfiable
    * (chromatic number, assignment) if k=None
    """

    def maxdegree(V, E):
        d = {}
        for m1, m2 in E:
            d[m1] = d.get(m1, 0) + 1
            d[m2] = d.get(m2, 0) + 1
        return max(d.values())

    kvar = Symbol('k', INT)
    vmap = {vname: Symbol(("v_%s" % str(vname)), INT) for vname in V}
    verts = [And(0 <= v, v < kvar) for v in vmap.values()]
    edges = [NotEquals(vmap[vi], vmap[vj]) for vi, vj in E]

    s = Solver()
    for v in verts:
        s.add_assertion(v)
    for e in edges:
        s.add_assertion(e)

    def result(model):
        return {vname: model[vmap[vname]] for vname in V}

    if k is not None:
        # attempt to color with k colors
        s.add_assertion(Equals(kvar, Int(k)))
        if s.solve():
            return result(s.get_model())
        else:
            return False
    else:
        # binary search for k
        mink = 1
        maxk = maxdegree(V, E) + 1

        model, minSATk = None, 0
        while mink <= maxk:
            s.push()
            k = int((mink + maxk) / 2)
            s.add_assertion(Equals(kvar, Int(k)))
            if s.solve():
                model, minSATk = s.get_model(), k
                maxk = k - 1
            else:
                mink = k + 1
            s.pop()

        return minSATk, result(model)


def chromatic_number(V, E):
    """ Returns the chromatic number of G(V, E). """
    k, cols = color(V, E, k=None)
    return k


if __name__ == '__main__':
    V = ['A', 'B', 'C', 'D']
    E = [('A', 'B'), ('A', 'C'), ('A', 'D'),
         ('B', 'D'), ('C', 'D')]
    print(color(V, E, 4))
    print(chromatic_number(V, E))
