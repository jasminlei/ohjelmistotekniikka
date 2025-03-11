import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_on_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_saldon_tulostus_nakyy_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_kortille_voi_ladata_saldoa(self):
        self.maksukortti.lataa_rahaa(2000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 30.0)

    def test_kortilta_voi_ottaa_rahaa(self):
        self.maksukortti.ota_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.0)

    def test_saldo_ei_muutu_jos_kortilta_yritetaan_ottaa_enemmän_kuin_saldo(self):
        self.maksukortti.ota_rahaa(1500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)

    def test_ota_rahaa_palauttaa_true_jos_rahat_riittavat(self):
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_ota_rahaa_palauttaa_false_jos_rahat_ei_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(1500), False)
