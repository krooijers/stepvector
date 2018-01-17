from stepvector import StepVector
from itertools import permutations



INTERVALS1 = [
    (100, 200, {"A1"}),
    (100, 220, {"A2"}),
    (100, 180, {"A3"}),
]

RES1 = [
    (100, 180, {"A1", "A2", "A3"}),
    (180, 200, {"A1", "A2"}),
    (200, 220, {"A2"}),
]

INTERVALS2 = [
    (400, 500, {"B1"}),
    (380, 500, {"B2"}),
    (420, 500, {"B3"}),
]

RES2 = [
    (380, 400, {"B2"}),
    (400, 420, {"B1", "B2"}),
    (420, 500, {"B1", "B2", "B3"}),
]

INTERVALS3 = [
    (1000, 2000, {"C1"}),
    (800, 2200, {"C2"}),
    (1200, 1800, {"C3"}),
]

RES3 = [
    (800, 1000, {"C2"}),
    (1000, 1200, {"C1", "C2"}),
    (1200, 1800, {"C1", "C2", "C3"}),
    (1800, 2000, {"C1", "C2"}),
    (2000, 2200, {"C2"}),
]


def test_intervals_add_value():
    yield do_intervals_add_value, INTERVALS1, RES1
    yield do_intervals_add_value, INTERVALS2, RES2
    yield do_intervals_add_value, INTERVALS3, RES3


def do_intervals_add_value(ivs, output):
    sv = StepVector(set)
    for start, end, val in ivs:
        sv.add_value(start, end, val)

    res = list(sv)
    assert res == output


def test_independence_of_order():
    yield do_independence_of_order, INTERVALS1, RES1
    yield do_independence_of_order, INTERVALS2, RES2
    yield do_independence_of_order, INTERVALS3, RES3


def do_independence_of_order(ivs, output):
    l = len(ivs)
    for order in permutations(range(l), l):
        sv = StepVector(set)
        for i in order:
            start, end, val = ivs[i]
            print(order, i, ivs[i], sv._t)
            sv.add_value(start, end, val)

        res = list(sv)
        assert res == output
