"""Test coordinates only; never consumed by the 6502 raster generator."""
BASE_X = [19,52,85,118,151]
BASE_Y = [72]*5
DENSE = [73,76,79,82,85]
SAME_Y = [75,74,73,72,71]


def cases(mode):
    if mode in ("one","single"):
        yield "one-base", BASE_X[:], BASE_Y[:], 3
        for delta in (0,3,6,0,-3,-6,0):
            x = BASE_X[:]
            x[0] = 25+delta
            yield f"one-x{delta:+d}", x, BASE_Y[:], 3
        for delta in (1,-1,0):
            y = BASE_Y[:]
            y[0] += delta
            yield f"one-y{delta:+d}", [25,*BASE_X[1:]], y, 3
        return
    if mode in ("rotate","rotatefine"):
        yield "dense-rotate", DENSE[:], BASE_Y[:], 20
        return
    yield "base-wide", BASE_X[:], BASE_Y[:], 6
    if mode == "wide":
        for actor in range(5):
            x = [3*(22+10*i+(1 if i==actor else 2 if i>actor else 0))-47 for i in range(5)]
            yield f"npc{actor}-base", x[:], BASE_Y[:], 2
            for delta in (3,-3):
                changed = x[:]
                changed[actor] += delta
                yield f"npc{actor}-x{delta:+d}", changed, BASE_Y[:], 2
            for delta in (1,-1):
                y = BASE_Y[:]
                y[actor] += delta
                yield f"npc{actor}-y{delta:+d}", x[:], y, 2
    for name,x,y,_ in soak()[1:]:
        yield name,x,y,4
    yield "reorder-requested", [127,19,73,100,46], [73,72,73,71,72], 4
    yield "separated-requested", [19,46,73,100,127], BASE_Y[:], 4
    yield "close3", DENSE[:], BASE_Y[:], 4
    yield "close1", [73,74,75,76,77], BASE_Y[:], 4
    yield "same-x-requested", [73,73,19,100,46], SAME_Y[:], 4
    yield "restored-wide", BASE_X[:], BASE_Y[:], 4


def soak():
    return [
        ("base-wide", BASE_X[:], BASE_Y[:], 150),
        ("reorder-wide", [151,19,85,118,52], [73,72,73,71,72], 150),
        ("staggered-wide", [52,151,19,118,85], [70,71,72,73,74], 150),
        ("same-x-feasible", [79,79,19,112,49], SAME_Y[:], 150),
    ]
