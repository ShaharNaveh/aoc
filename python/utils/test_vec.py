import unittest

from . import Vec2, Vec3


class Vec2Tests(unittest.TestCase):
    def test_ops(self):
        a = Vec2(3, -4)
        self.assertEqual(a + Vec2.ONE, Vec2(4, -3))
        self.assertEqual(a - Vec2.X, Vec2(2, -4))
        self.assertEqual(a * 2, Vec2(6, -8))
        self.assertEqual(a * Vec2(2, 3), Vec2(6, -12))
        self.assertEqual(-a, Vec2(-3, 4))
        self.assertEqual(Vec2(-7, 7) / 2, Vec2(-3, 3))

    def test_helpers(self):
        a = Vec2(3, -4)
        self.assertEqual(a.abs(), Vec2(3, 4))
        self.assertEqual(a.signum(), Vec2(1, -1))
        self.assertEqual(a.element_sum(), -1)
        self.assertEqual(a.element_product(), -12)
        self.assertEqual(a.min(Vec2(0, 0)), Vec2(0, -4))
        self.assertEqual(a.max(Vec2(0, 0)), Vec2(3, 0))
        self.assertEqual(a.with_y(1), Vec2(3, 1))
        self.assertEqual(Vec2.X.rotate(Vec2.Y), Vec2.Y)

    def test_neighbors(self):
        self.assertEqual(len(set(Vec2.ZERO.neighbors_4())), 4)
        self.assertEqual(len(set(Vec2.ZERO.neighbors_8())), 8)
        self.assertIn(Vec2(2, 2), Vec2.ONE.neighbors_8())


class Vec3Tests(unittest.TestCase):
    def test_ops(self):
        a = Vec3.from_str(" 1, -2,3")
        self.assertEqual(a, Vec3(1, -2, 3))
        self.assertEqual(a + Vec3.splat(1), Vec3(2, -1, 4))
        self.assertEqual(a - a, Vec3.ZERO)
        self.assertEqual(a * 2, Vec3(2, -4, 6))
        self.assertEqual(a.abs().element_sum(), 6)
        self.assertEqual(a.length_squared(), 14)
        self.assertEqual(a.distance_squared(Vec3.ZERO), 14)
