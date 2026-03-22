import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_kassapaate_on_luotu_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_edullinen_kasvattaa_kassaa(self):
        kateinen = self.kassapaate.syo_edullisesti_kateisella(245)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(kateinen, 5)

    def test_kateisosto_edullinen_ei_kasvata_kassaa_jos_rahaa_ei_riita(self):
        kateinen = self.kassapaate.syo_edullisesti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(kateinen, 100)

    def test_kateisosto_maukas_kasvattaa_kassaa(self):
        kateinen = self.kassapaate.syo_maukkaasti_kateisella(405)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.0)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(kateinen, 5)

    def test_kateisosto_maukas_ei_kasvata_kassaa_jos_rahaa_ei_riita(self):
        kateinen = self.kassapaate.syo_maukkaasti_kateisella(100)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(kateinen, 100)

    def test_korttiosto_edullinen_vahentaa_kortin_saldoa(self):
        kortti_osto = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 760)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(kortti_osto, True)

    def test_korttiosto_edullinen_ei_vahentaa_kortin_saldoa_jos_rahaa_ei_riita(self):
        self.kortti.ota_rahaa(999)
        kortti_osto = self.kassapaate.syo_edullisesti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(kortti_osto, False)

    def test_korttiosto_maukas_vahentaa_kortin_saldoa(self):
        kortti_osto = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 600)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(kortti_osto, True)

    def test_korttiosto_maukas_ei_vahentaa_kortin_saldoa_jos_rahaa_ei_riita(self):
        self.kortti.ota_rahaa(999)
        kortti_osto = self.kassapaate.syo_maukkaasti_kortilla(self.kortti)
        self.assertEqual(self.kortti.saldo, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(kortti_osto, False)

    def test_kortille_lataaminen_kasvattaa_kortin_ja_kassan_saldoa(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)
        self.assertEqual(self.kortti.saldo, 1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005.0)
    
    def test_kortille_lataaminen_ei_kasvata_kortin_ja_kassan_saldoa_jos_summa_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -500)
        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)