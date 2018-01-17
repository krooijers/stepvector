from stepvector import StepVector
from itertools import permutations


def test_edgecases_half_set_slice_1():
    sv = StepVector(set)
    sv[100:200] = {"A"}

    assert list(sv[50:250]) == [(50, 100, set()), (100, 200, {"A"}), (200, 250, set())]

    assert list(sv[:220]) == [(100, 200, {"A"}), (200, 220, set())]
    assert list(sv[150:]) == [(150, 200, {"A"})]
    assert list(sv[200:]) == []
    assert list(sv[1000:]) == []


def test_edgecases_half_set_slice_2():
    sv = StepVector(set)
    sv[100:200] = {"A"}
    sv[400:500] = {"B"}

    assert list(sv[50:250]) == [(50, 100, set()), (100, 200, {"A"}), (200, 250, set())]
    assert list(sv[350:550]) == [(350, 400, set()), (400, 500, {"B"}), (500, 550, set())]

    assert list(sv[50:100]) == [(50, 100, set())]

    assert list(sv[50:50]) == []
    assert list(sv[320:320]) == []

    assert list(sv[:100]) == []
    assert list(sv[:300]) == [(100, 200, {"A"}), (200, 300, set())]
    assert list(sv[:400]) == [(100, 200, {"A"}), (200, 400, set())]
    assert list(sv[:500]) == [(100, 200, {"A"}), (200, 400, set()), (400, 500, {"B"})]
    assert list(sv[100:]) == [(100, 200, {"A"}), (200, 400, set()), (400, 500, {"B"})]
    assert list(sv[500:]) == []
