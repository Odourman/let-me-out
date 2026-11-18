"""Frozen and seeded runtime coordinate fixtures."""
from random import Random

BASE_X = [55,91,130,24,26]
BASE_Y = [72]*5

def cases(mode):
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

def seeded():
    rng = Random(0x6507_35)
    for index in range(12):
        if index < 6:
            clocks = [rng.randint(22,24)]
            for minimum in (8,8,8,9):
                clocks.append(clocks[-1] + minimum)
            for _ in range(58-clocks[-1]):
                gap = rng.choice(range(1,5))
                clocks = [clock+(i>=gap) for i,clock in enumerate(clocks)]
            # Vary the right edge as well as interior gaps.
            if index % 2 == 0:
                clocks[-1] -= int(clocks[-1]-clocks[-2]>9)
            order = [0,1,*rng.sample([2,3,4],3)]
        else:
            clocks = [22]
            for _ in range(4):
                clocks.append(clocks[-1]+rng.choice((10,11)))
            order = rng.sample(range(5),5)
        x, y = [0]*5, [rng.randint(67,76) for _ in range(5)]
        if index < 6:
            y[1] = y[0]
        for actor,clock in zip(order,clocks):
            x[actor] = 3*clock-47
        yield f"seed-{index:02d}", x,y,3
    for index in range(4):
        x = rng.sample(range(65,77),5)
        y = [rng.randint(68,75) for _ in range(5)]
        yield f"seed-dense-{index}",x,y,3
    for residue in range(3):
        yield f"anchor-residue-{residue}", [19+residue,52,85,118,151], BASE_Y[:], 3

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
