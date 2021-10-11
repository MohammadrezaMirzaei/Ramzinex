import unittest
from python_ramzinex_api.ramzinex import Client


class RamzinexTestCase(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_0(self):
        """Test get_markets"""
        # get tether/rial market
        result = self.client.get_markets(pair_id=11)
        self.assertEqual(result["status"], 0)

    def test_1(self):
        """Test get_prices"""
        result = self.client.get_prices()
        self.assertEqual(result["status"], 0)

    def test_2(self):
        """Test get_markets_turnover"""
        result = self.client.get_markets_turnover()
        self.assertEqual(result["status"], 0)

    def test_3(self):
        """Test get_orderbook"""
        result = self.client.get_orderbook(pair_id=11, side="buys")
        self.assertEqual(result["status"], 0)


if __name__ == '__main__':
    unittest.main()