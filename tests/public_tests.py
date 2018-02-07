from unittest import TestCase, main as unittest_go
from pprint import pprint
import math
import time

from quadriga import QCX
from config import TRADE_PAIRS, CURRENT_TRADE_INFORMATION_COMPONENTS

class TestPublicAPI(TestCase):
    def setUp(self):
        self.qcx = QCX('../config/sample.cfg') # config is unimportant for public calls.
        self.verbose = False

    def test_current_trading_information(self):
        time.sleep(60)
        data = self.qcx.api('ticker')

        if self.verbose:
            pprint(data)

        for trade_pair, trade_pair_cti in data.items():
            self.assertIn(trade_pair, TRADE_PAIRS)
            self.assertNotIn('error', trade_pair_cti.keys())

            for cti_component in CURRENT_TRADE_INFORMATION_COMPONENTS:
                self.assertIn(cti_component, trade_pair_cti.keys())
                self.assertIsInstance(trade_pair_cti[cti_component], str)
                self.assertIsInstance(float(trade_pair_cti[cti_component]), float)

    def test_order_book(self):
        time.sleep(60)
        data = self.qcx.api('order_book')

        if self.verbose:
            pprint(data)

        for trade_pair, trade_pair_order_book in data.items():
            self.assertIn(trade_pair, TRADE_PAIRS)
            self.assertNotIn('error', trade_pair_order_book.keys())

            for order_type, order_book in trade_pair_order_book.items():
                self.assertIn(order_type, ['asks', 'bids', 'timestamp'])

                if order_type == 'timestamp':
                    timestamp = order_book
                    self.assertIsInstance(timestamp, str)
                    self.assertIsInstance(int(timestamp), int)
                    self.assertTrue(math.floor(float(timestamp)) == int(timestamp))

                elif order_type in ['asks', 'bids']:
                    for order in order_book:
                        self.assertTrue(len(order) == 2)

                        self.assertIsInstance(order[0], str)
                        self.assertIsInstance(order[1],str)
                        self.assertIsInstance(float(order[0]), float)
                        self.assertIsInstance(float(order[1]), float)

    def test_transactions(self):
        time.sleep(60)
        data = self.qcx.api('transactions')
        if self.verbose:
            pprint(data)

        for trade_pair, trade_pair_transactions in data.items():
            self.assertIn(trade_pair, TRADE_PAIRS)
            if len(trade_pair_transactions) > 0:
                self.assertNotIn('error', trade_pair_transactions[0].keys())

                for transaction in trade_pair_transactions:
                    for key, value in transaction.items():
                        self.assertIn(key, ['amount', 'price', 'date', 'side', 'tid'])

                        if key == 'tid':
                            self.assertIsInstance(value, int)
                        else:
                            self.assertIsInstance(value, str)

                            if key == 'date':
                                self.assertTrue(math.floor(float(value)) == math.ceil(float(value)))
                            elif key in ['amount', 'price']:
                                if not value.endswith('0' * len(value[value.find('.')+1:])): # Floats that end in 0s are integers
                                    self.assertFalse(math.floor(float(value)) == math.ceil(float(value)))


if __name__ == "__main__":
    unittest_go()