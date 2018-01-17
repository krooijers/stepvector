from stepvector import StepVector
from itertools import permutations



INTERVALS = [
    (200, 300, {"A"}),
    (400, 500, {"B"}),
    (450, 550, {"B2"}),
    (50, 150, {"0"}),
    (150, 220, {"A0"}),
    (20, 320, {"L"}),
]

RES = [
    (20, 50, {"L"}),
    (50, 150, {"L", "0"}),
    (150, 200, {"L", "A0"}),
    (200, 220, {"L", "A0", "A"}),
    (220, 300, {"L", "A"}),
    (300, 320, {"L"}),
    (320, 400, set()),
    (400, 450, {"B"}),
    (450, 500, {"B", "B2"}),
    (500, 550, {"B2"}),
]

def test_intervals_add_value():
    sv = StepVector(set)
    for start, end, val in INTERVALS:
        sv.add_value(start, end, val)

    res = list(sv)
    assert res == RES

def test_independence_of_order():
    l = len(INTERVALS)
    for order in permutations(range(l), l):
        sv = StepVector(set)
        for i in order:
            start, end, val = INTERVALS[i]
            print(order, i, INTERVALS[i], sv._t)
            sv.add_value(start, end, val)

        res = list(sv)
        assert res == RES
