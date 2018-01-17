from stepvector import StepVector
from itertools import permutations



INTERVALS = [
    (100, 200, {"A1"}),
    (100, 220, {"A2"}),
    (100, 180, {"A3"}),
]


def test_get_and_slice_operations():
    sv = StepVector(set)
    for start, end, val in INTERVALS:
        sv.add_value(start, end, val)

    assert list(sv[0:100]) == [(0, 100, set())]
    assert list(sv[0:200]) == [(0, 100, set()), (100, 180, {"A1", "A2", "A3"}), (180, 200, {"A1", "A2"})]
    assert list(sv[150:250]) == [(150, 180, {"A1", "A2", "A3"}), (180, 200, {"A1", "A2"}), (200, 220, {"A2"}), (220, 250, set())]
