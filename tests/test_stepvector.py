import importcontext
from stepvector import StepVector
import pytest


BASIC_INT_DATA = [
    (0, 100, 1),
    (1000, 1100, 2),
    (2000, 2100, 3),
]


class TestBasicInt:
    @classmethod
    def setup_class(cls):
        sv = StepVector(int)
        for (start, end, value) in BASIC_INT_DATA:
            sv[start:end] = value

        cls.sv = sv

    def test_basic_ivs(self):
        l = list(self.sv[0:10])
        assert len(l) == 1
        assert l[0][2] == 1

        l = list(self.sv[0:100])
        assert len(l) == 1
        assert l[0][2] == 1

        l = list(self.sv[0:101])
        assert len(l) == 2
        assert l[0][2] == 1
        assert l[1][2] == 0

        l = list(self.sv)
        assert len(l) == 5
        assert sum((end - start) for (start, end, value) in l if value > 0) == 300
        assert sum(value * (end - start) for (start, end, value) in l) == 600
        assert all((type(value) == int for (_, _, value) in l))

    def test_basic_pos(self):
        assert self.sv[-1] == 0
        assert self.sv[0] == 1
        assert self.sv[1] == 1
        assert self.sv[100] == 0

        assert self.sv[999] == 0
        assert self.sv[1000] == 2
        assert self.sv[1099] == 2
        assert self.sv[1100] == 0

    def test_halfopen_ivs(self):
        l = list(self.sv[:10])
        assert len(l) == 1
        assert l[0][2] == 1

    def test_bounded(self):
        sv2 = self.sv[10:20]
        l = list(sv2)
        assert len(l) == 1
        assert l[0][2] == 1

    def test_semi_bounded(self):
        sv2 = self.sv[10:]
        l = list(sv2[:100])
        assert len(l) == 1
        assert l[0][2] == 1

        sv2 = self.sv[:100]
        l = list(sv2[10:])
        assert len(l) == 1
        assert l[0][2] == 1

    def test_setitem(self):
        sv = StepVector(int)
        sv[0:100] = 1

        l = list(sv[0:200])
        assert len(l) == 2

        sv[50] = 2
        l = list(sv[0:200])
        print(l)
        assert len(l) == 4  # [0, 50), [50, 51), [51, 100), [100, 200)
        assert sv[50] == 2

    def test_setitem_emptyslice(self):
        sv = StepVector(int)
        sv[0:100] = 1

        l = list(sv[0:200])
        assert len(l) == 2

        sv[50:50] = 123

        l = list(sv[0:200])
        assert len(l) == 2

    def test_addvalue_nonset(self):
        l = list(self.sv[0:200])
        assert len(l) == 2

        self.sv.add_value(50, 50, 123)

        l = list(self.sv[0:200])
        assert len(l) == 2

        self.sv.add_value(50, 51, 1)

        l = list(self.sv[0:200])
        assert len(l) == 4


BASIC_SET_DATA = [
    (0, 100, "A"),
    (1000, 1100, "B"),
    (2000, 2100, "C"),
]


class TestBasicSet:
    @classmethod
    def setup_class(cls):
        sv = StepVector(set)
        for (start, end, value) in BASIC_SET_DATA:
            sv.add_value(start, end, {value})

        cls.sv = sv

    def test_basic_ivs(self):
        l = list(self.sv[0:10])
        assert len(l) == 1
        assert l[0][2] == {"A"}

        l = list(self.sv[0:100])
        assert len(l) == 1
        assert l[0][2] == {"A"}

        l = list(self.sv[0:101])
        assert len(l) == 2
        assert l[0][2] == {"A"}
        assert l[1][2] == set()

        l = list(self.sv)
        assert len(l) == 5
        assert sum((end - start) for (start, end, value) in l if value) == 300
        assert all((type(value) == set for (_, _, value) in l))

    def test_basic_pos(self):
        assert self.sv[-1] == set()
        assert self.sv[0] == {"A"}
        assert self.sv[1] == {"A"}
        assert self.sv[100] == set()

        assert self.sv[999] == set()
        assert self.sv[1000] == {"B"}
        assert self.sv[1099] == {"B"}
        assert self.sv[1100] == set()


OVERLAPPING_SET_DATA = [
    (0, 100, "A"),
    (1000, 1100, "B1"),
    (1050, 1150, "B2"),
    (2000, 2100, "C"),
]


class TestOverlappingSet:
    @classmethod
    def setup_class(cls):
        sv = StepVector(set)
        for (start, end, value) in OVERLAPPING_SET_DATA:
            sv.add_value(start, end, {value})

        cls.sv = sv

    def test_basic_ivs(self):
        l = list(self.sv[0:10])
        assert len(l) == 1
        assert l[0][2] == {"A"}

        l = list(self.sv[0:100])
        assert len(l) == 1
        assert l[0][2] == {"A"}

        l = list(self.sv[0:101])
        assert len(l) == 2
        assert l[0][2] == {"A"}
        assert l[1][2] == set()

        l = list(self.sv)
        assert len(l) == 7
        assert sum((end - start) for (start, end, value) in l if value) == 350
        assert all((type(value) == set for (_, _, value) in l))

    def test_basic_pos(self):
        assert self.sv[-1] == set()
        assert self.sv[0] == {"A"}
        assert self.sv[1] == {"A"}
        assert self.sv[100] == set()

        assert self.sv[999] == set()
        assert self.sv[1000] == {"B1"}
        assert self.sv[1049] == {"B1"}
        assert self.sv[1050] == {"B1", "B2"}
        assert self.sv[1099] == {"B1", "B2"}
        assert self.sv[1100] == {"B2"}
        assert self.sv[1150] == set()


class TestInvalid:
    @classmethod
    def setup_class(cls):
        sv = StepVector(int)
        for (start, end, value) in BASIC_INT_DATA:
            sv[start:end] = value

        cls.sv = sv

    def test_invalid_getitem(self):
        with pytest.raises(ValueError, match="Invalid step value"):
            self.sv[0:2:2]

    def test_outofbounds(self):
        sv2 = self.sv[10:20]
        assert sv2[10] == 1
        assert sv2[19] == 1

        with pytest.raises(ValueError, match="bounds"):
            sv2[5:25]

        with pytest.raises(ValueError, match="bounds"):
            sv2[5:]

        with pytest.raises(ValueError, match="bounds"):
            sv2[:25]

        with pytest.raises(ValueError, match="bounds"):
            sv2[20]

        sv2 = self.sv[500:600]
        assert sv2[500] == 0
        assert sv2[599] == 0

        with pytest.raises(ValueError, match="bounds"):
            sv2[400:700]

        with pytest.raises(ValueError, match="bounds"):
            sv2[400:600]

        with pytest.raises(ValueError, match="bounds"):
            sv2[499]

        with pytest.raises(ValueError, match="bounds"):
            sv2[600]


class TestEmpty:
    def test_1(self):
        sv = StepVector(int)
        l = list(sv[:])
        assert len(l) == 0

        sv = StepVector(int)
        l = list(sv[-100:100])
        assert len(l) == 1
        assert l[0][2] == 0
