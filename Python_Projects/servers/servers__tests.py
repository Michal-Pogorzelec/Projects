import unittest
from collections import Counter

from servers import *

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_get_entries_throws_exception(self):
        products = [Product('P12', 1), Product('PP234', 2),Product('PA234', 25),
                    Product('PD234', 22),Product('ED234', 21)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                entries = server.get_entries(2)

    def test_get_entries_not_throws_exception_for_3_elements(self):
        products = [Product('P12', 1), Product('PA234', 1), Product('PD234', 3),Product('ED234', 2)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[1], products[3], products[2]]), Counter(entries))


class ClientTest(unittest.TestCase):
    def test_total_price_for_execution_with_too_many_products(self):
        products = [Product('PD12', 1), Product('P254', 1), Product('P224', 2),
                    Product('P114', 4), Product('E254', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(1))

    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))


    def test_total_price_for_no_products_meeting_the_criteria(self):
        products = [Product('PP234', 2), Product('PD235', 3), Product('PA225', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(1))


if __name__ == '__main__':
    unittest.main()