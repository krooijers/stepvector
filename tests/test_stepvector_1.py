from stepvector import StepVector


INTERVALS1 = [
    (100, 200, {"A"}),
    (300, 400, {"B"}),
]
RES1 = [
    (100, 200, {"A"}),
    (200, 300, set()),
    (300, 400, {"B"}),
]


def test_intervals1_add_value():
    sv = StepVector(set)
    for start, end, val in INTERVALS1:
        sv.add_value(start, end, val)

    res = list(sv)
    assert res == RES1


def test_intervals1_set():
    sv = StepVector(set)
    for start, end, val in INTERVALS1:
        sv[start:end] = val

    res = list(sv)
    assert res == RES1


INTERVALS2 = [
    (100, 200, {"A"}),
    (200, 300, {"B"}),
]
RES2 = [
    (100, 200, {"A"}),
    (200, 300, {"B"}),
]


def test_intervals2_add_value():
    sv = StepVector(set)
    for start, end, val in INTERVALS2:
        sv.add_value(start, end, val)

    res = list(sv)
    assert res == RES2


def test_intervals2_set():
    sv = StepVector(set)
    for start, end, val in INTERVALS2:
        sv[start:end] = val

    res = list(sv)
    assert res == RES2


INTERVALS3 = [
    (100, 200, {"A"}),
    (200, 300, {"A"}),
]
RES3 = [
    (100, 300, {"A"}),
]


def test_intervals3_add_value():
    sv = StepVector(set)
    for start, end, val in INTERVALS3:
        sv.add_value(start, end, val)

    res = list(sv)
    assert res == RES3


def test_intervals3_set():
    sv = StepVector(set)
    for start, end, val in INTERVALS3:
        sv[start:end] = val

    res = list(sv)
    assert res == RES3


INTERVALS4 = [
    (100, 200, {"A"}),
    (50, 100, {"A"}),
]
RES4 = [
    (50, 200, {"A"}),
]


def test_intervals4_add_value():
    sv = StepVector(set)
    for start, end, val in INTERVALS4:
        sv.add_value(start, end, val)

    res = list(sv)
    assert res == RES4


def test_intervals4_set():
    sv = StepVector(set)
    for start, end, val in INTERVALS4:
        sv[start:end] = val

    res = list(sv)
    assert res == RES4

