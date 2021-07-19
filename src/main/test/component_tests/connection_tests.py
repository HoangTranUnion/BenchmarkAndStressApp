import unittest
from src.main.MainComponents.connection import Connection


class TestConnection(unittest.TestCase):
    def test_ip_connection(self):
        ip = '1.1.1.1'
        self.assertEqual(Connection.ip_status(ip), 0, "Cloudflare's IP should have ping result as 0")
        ip_2 = '1.35.5.33'
        self.assertTrue(Connection.ip_status(ip_2) > 0, "This random IP should not be able to be connected.")

    def test_doh_connection(self):
        doh_1 = 'https://cloudflare-dns.com/dns-query'
        doh_2 = 'https://randomples.sus/dns-query'
        doh_3 = 'randomples.sus'
        doh_4 = 'cloudflare-dns.com/dns-query'

        self.assertEqual(Connection.domain_status(doh_1, 'doh'), 0, "Cloudflare's DoH URL should have ping result as 0")
        self.assertEqual(Connection.domain_status(doh_4,'doh'),0, "Cloudflare's DoH URL should have ping result as 0")
        self.assertTrue(Connection.domain_status(doh_2, 'doh') > 0, "This random domain should either have ping result to be 1 or 2")
        self.assertTrue(Connection.domain_status(doh_3,'doh') > 0, "This random domain should either have ping result to be 1 or 2")

    def test_constructor(self):
        self.assertRaises(AssertionError, Connection(None,'fb.com'))



if __name__ == '__main__':
    unittest.main()