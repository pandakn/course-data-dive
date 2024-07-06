import unittest


class TestArithmetic(unittest.TestCase):
	def test_subtract(self):
		"""Test that 2 minus 1 equals 1."""
		result = 2 - 1
		self.assertEqual(result, 1)


if __name__ == '__main__':
	unittest.main()
