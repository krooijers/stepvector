from stepvector import StepVector
from itertools import permutations


def test_edgecases_empty_1():
    sv = StepVector(set)
    assert list(sv[0:100]) == [(0, 100, set())]


def test_edgecases_empty_2():
    sv = StepVector(set)
    assert list(sv[-200:-100]) == [(-200, -100, set())]


def test_edgecases_empty_slice_1():
    sv = StepVector(set)
    sv[100:200] = {"A"}
    assert list(sv[50:250]) == [(50, 100, set()), (100, 200, {"A"}), (200, 250, set())]
    assert list(sv[200:220]) == [(200, 220, set())]
    assert list(sv[220:220]) == []
    assert list(sv[10:20]) == [(10, 20, set())]
    assert list(sv[10:10]) == []


def test_edgecases_noninteger_keys_1():
    sv = StepVector(set)
    assert list(sv[-3.14:2.78]) == [(-3.14, 2.78, set())]


def test_edgecases_noninteger_keys_2():
    sv = StepVector(set)
    assert list(sv[(3, 4):(3, 5)]) == [((3, 4), (3, 5), set())]
    assert list(sv[(3, 4):(4, 1)]) == [((3, 4), (4, 1), set())]


def test_edgecases_noninteger_keys_2():
    sv = StepVector(set)
    assert list(sv[(3, 4):(2, 10)]) == []  # NB: end < start
