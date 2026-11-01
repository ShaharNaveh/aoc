import unittest

from .vec import Vec2, Vec3


class TestVec2(unittest.TestCase):
    def test_arithmetic(self):
        a = Vec2(3, -4)
        self.assertEqual(a + Vec2(1, 1), Vec2(4, -3))
        self.assertEqual(a - Vec2(1, 0), Vec2(2, -4))
        self.assertEqual(a * 2, Vec2(6, -8))
        self.assertEqual(2 * a, Vec2(6, -8))
        self.assertEqual(Vec2(-7, 7) // 2, Vec2(-4, 3))
        self.assertEqual(-a, Vec2(-3, 4))
        self.assertEqual(abs(a), Vec2(3, 4))

    def test_unpacking(self):
        x, y = Vec2(1, 2)
        self.assertEqual((x, y), (1, 2))

    def test_manhattan(self):
        self.assertEqual(Vec2(3, -4).manhattan(), 7)
        self.assertEqual(Vec2(3, -4).manhattan(Vec2(1, 1)), 7)

    def test_neighbors(self):
        self.assertEqual(len(set(Vec2(0, 0).neighbors())), 4)
        self.assertEqual(len(set(Vec2(0, 0).neighbors(diagonals=True))), 8)
        self.assertIn(Vec2(2, 2), Vec2(1, 1).neighbors(diagonals=True))


class TestVec3(unittest.TestCase):
    def test_from_str(self):
        self.assertEqual(Vec3.from_str("1,-2,3"), Vec3(1, -2, 3))

    def test_arithmetic(self):
        a = Vec3(1, -2, 3)
        self.assertEqual(a + Vec3(1, 1, 1), Vec3(2, -1, 4))
        self.assertEqual(a - a, Vec3(0, 0, 0))
        self.assertEqual(a * 2, Vec3(2, -4, 6))
        self.assertEqual(a.dot(a), 14)
        self.assertEqual(a.manhattan(), 6)
