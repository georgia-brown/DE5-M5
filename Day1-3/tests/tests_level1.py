import unittest
from calculator import calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calculation = calculator(2,2)
        self.assertEqual(calculation.get_sum(), 4, "The sum is wrong")

    def test_diff(self):
        calculation = calculator(2,2)
        self.assertEqual(calculation.get_diff(), 0, "The diference is wrong")

    def test_product(self):
        calculation = calculator(2,2)
        self.assertEqual(calculation.get_product(), 4, "The product is wrong")

    def test_quotient(self):
        calculation = calculator(2,2)
        self.assertEqual(calculation.get_quotient(), 1, "The quotient is wrong")

if __name__ == "__main__":

    unittest.main()