import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(10)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)
    
    def test_the_card_returns_its_current_value(self):
        self.assertEqual(self.maksukortti.__str__(), "saldo: 0.1")
    
    def test_money_can_be_stored_on_the_card(self):
        self.maksukortti.lataa_rahaa(10)
        self.assertEqual(self.maksukortti.__str__(), "saldo: 0.2")
    
    def test_money_can_be_withdrawn_from_the_card(self):
        self.maksukortti.ota_rahaa(5)
        self.assertEqual(self.maksukortti.__str__(), "saldo: 0.05")

    def test_the_balance_cannot_become_negative(self):
        self.maksukortti.ota_rahaa(11)
        self.assertEqual(self.maksukortti.__str__(), 'saldo: 0.1')