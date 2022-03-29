import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti
class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(420)

    def test_checkout_status_is_correct(self):
        money = self.kassapaate.kassassa_rahaa
        sold = self.kassapaate.edulliset + self.kassapaate.maukkaat
        self.assertEqual(str(money)+','+str(sold), "100000,0")
    def test_with_sufficient_cash_payment_affordble_lunch_is_bought_with_correct_change_returned(self):
        change=0
        change+=self.kassapaate.syo_edullisesti_kateisella(50)
        change+=self.kassapaate.syo_edullisesti_kateisella(250)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa)+','+str(change)+','+str(self.kassapaate.edulliset), str(100240)+','+str(60)+','+str(1))
    def test_with_sufficient_cash_payment_tasty_lunch_is_bought_with_correct_change_returned(self):
        change=0
        change+=self.kassapaate.syo_maukkaasti_kateisella(50)
        change+=self.kassapaate.syo_maukkaasti_kateisella(410)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa)+','+str(change)+','+str(self.kassapaate.maukkaat), str(100400)+','+str(60)+','+str(1))
    def test_with_sufficient_card_payment_affordble_lunch_is_bought_and_True_returned(self):
        p1=self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        p2=self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(str(p1)+','+str(p2)+','+str(self.kassapaate.edulliset)+','+str(self.kortti.saldo), 'True,False,1,180')
    def test_with_sufficient_card_payment_tasty_lunch_is_bought_and_True_returned(self):
        p1=self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        p2=self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(str(p1)+','+str(p2)+','+str(self.kassapaate.maukkaat)+','+str(self.kortti.saldo), 'True,False,1,20')
    def test_cashpayment_increases_register_and_card_balance(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -1)
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 200)
        self.assertEqual(str(self.kassapaate.kassassa_rahaa)+','+str(self.kortti.saldo),'100200,620')