"""Runtime coordinate fixtures. The pair ROM uses NPC IDs 3 and 4 geometrically."""
BASE_X = [55,91,130,24,26]
BASE_Y = [72]*5

def cases(mode):
    if mode in ("pair","rowprobe"):
        for dx in range(1,9):
            for dy in range(3):
                yield f"dx{dx}-dy{dy}", [19,52,151,73,73+dx], [72,72,72,72,72+dy], 2
        for x in (72,73,74):
            yield f"residue-{x%3}", [19,52,151,x,x+1], [72,72,72,72,73], 2
        yield "reverse-pair", [19,52,151,74,72], [72,72,72,72,73], 2
        return
    yield from [(name,x,y,3) for name,x,y,_ in soak()]
    for actor in range(5):
        x, y = BASE_X[:], BASE_Y[:]
        delta = 3 if actor < 3 else 1
        if actor == 3:
            x[3], x[4] = 25, 24
        elif actor == 4:
            x[4] = 25
        yield f"id{actor}-base", x, y, 2
        for step in (-delta, delta):
            moved = x[:]
            moved[actor] += step
            yield f"id{actor}-x{step:+d}", moved, y, 2
        for step in (-1, 1):
            moved = y[:]
            moved[actor] += step
            yield f"id{actor}-y{step:+d}", x, moved, 2
    yield "wide-control", [19,52,85,118,151], BASE_Y[:], 3
    yield "historic-reorder", [127,19,73,100,46], [73,72,73,71,72], 3
    yield "historic-close3", [73,76,79,82,85], BASE_Y[:], 3
    yield "historic-close1", [73,74,75,76,77], BASE_Y[:], 3
    yield "historic-samex", [73,73,19,100,46], [75,74,73,72,71], 3

def soak():
    return [
        ("historic-separated", [19,46,73,100,127], BASE_Y[:], 100),
        ("slack-separated", [19,46,76,118,145], BASE_Y[:], 100),
        ("slack-reorder", [145,19,76,118,46], [73,72,73,71,72], 100),
        ("close2", BASE_X[:], BASE_Y[:], 60),
        ("close1", [55,91,130,24,25], [72,72,72,71,73], 60),
        ("reorder", [91,130,55,26,24], [73,72,70,72,74], 60),
        ("samex", [55,91,130,24,24], [72,72,72,71,73], 60),
        ("two-pairs", [70,70,130,24,26], [71,73,72,71,73], 60),
    ]
