import unittest
import python_ramzinex_api.ramzinex


class RamzinexTestCase(unittest.TestCase):

    def setUp(self):
        self.public_api = python_ramzinex_api.ramzinex.PublicAPI()

    def test_zero(self):
        """Test get_markets"""
        # get tether/rial market
        result = self.public_api.get_markets(11)
        self.assertEqual(result["status"], 0)


if __name__ == '__main__':
    unittest.main()