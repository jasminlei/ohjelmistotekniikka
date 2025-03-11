import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)
        self.kortti_liian_vahan_saldoa = Maksukortti(100)

    def kassan_saldo_kasvaa(self, funktio, summa, odotettu_saldo, kortti=None):
        if kortti:
            funktio(kortti, summa)
        else:
            funktio(summa)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), odotettu_saldo)

    def vaihtoraha_oikein(self, funktio, maksu, odotettu_vaihtoraha):
        self.assertEqual(funktio(maksu), odotettu_vaihtoraha)

    def myytyjen_lounaiden_maara_oikein(
        self, funktio, odotettu_maara, lounastyyppi, kortti=None, summa=None
    ):
        if kortti:
            funktio(kortti)
            self.assertEqual(getattr(self.kassapaate, lounastyyppi), odotettu_maara)
        else:
            funktio(summa)
            self.assertEqual(getattr(self.kassapaate, lounastyyppi), odotettu_maara)

    def kortin_saldo_oikein(self, funktio, kortti, odotettu_saldo, summa=None):
        if summa:
            funktio(kortti, summa)
            self.assertEqual(kortti.saldo_euroina(), odotettu_saldo)
        else:
            funktio(kortti)
            self.assertEqual(kortti.saldo_euroina(), odotettu_saldo)

    def test_kassan_saldo_on_oikea_alussa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.0)

    def test_myytyjen_edullisten_lounaiden_maara_on_alussa_nolla(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_myytyjen_maukkaiden_lounaiden_maara_on_alussa_nolla(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_kasvattaa_kassan_saldoa_edullisesti(self):
        self.kassan_saldo_kasvaa(
            self.kassapaate.syo_edullisesti_kateisella, 300, 1002.40
        )

    def test_kateisosto_kasvattaa_kassan_saldoa_maukkaasti(self):
        self.kassan_saldo_kasvaa(
            self.kassapaate.syo_maukkaasti_kateisella, 500, 1004.00
        )

    def test_kateisosto_vaihtoraha_oikein_edullisesti(self):
        self.vaihtoraha_oikein(self.kassapaate.syo_edullisesti_kateisella, 300, 60)

    def test_kateisosto_vaihtoraha_oikein_maukkaasti(self):
        self.vaihtoraha_oikein(self.kassapaate.syo_maukkaasti_kateisella, 500, 100)

    def test_kateisosto_kasvattaa_myytyjen_edullisten_lounaiden_maaraa(self):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_edullisesti_kateisella, 1, "edulliset", 500
        )

    def test_kateisosto_kasvattaa_myytyjen_maukkaiden_lounaiden_maaraa(self):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_maukkaasti_kateisella, 1, "maukkaat", 500
        )

    def test_kateisosto_ei_muuta_kassaa_jos_maksu_ei_riita_edullisesti(self):
        self.kassan_saldo_kasvaa(
            self.kassapaate.syo_edullisesti_kateisella, 100, 1000.0
        )

    def test_kateisosto_ei_muuta_kassaa_jos_maksu_ei_riita_maukkaasti(self):
        self.kassan_saldo_kasvaa(self.kassapaate.syo_maukkaasti_kateisella, 100, 1000.0)

    def test_kateisosto_palauttaa_koko_summan_jos_maksu_ei_riita_edullisesti(self):
        self.vaihtoraha_oikein(self.kassapaate.syo_edullisesti_kateisella, 100, 100)

    def test_kateisosto_palauttaa_koko_summan_jos_maksu_ei_riita_maukkaasti(self):
        self.vaihtoraha_oikein(self.kassapaate.syo_maukkaasti_kateisella, 100, 100)

    def test_kateisosto_ei_kasvata_myytyjen_edullisten_lounaiden_maaraa_jos_maksu_ei_riita(
        self,
    ):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_edullisesti_kateisella, 0, "edulliset", 100
        )

    def test_kateisosto_ei_kasvata_myytyjen_maukkaiden_lounaiden_maaraa_jos_maksu_ei_riita(
        self,
    ):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_maukkaasti_kateisella, 0, "maukkaat", 100
        )

    def test_korttimaksu_jos_kortilla_tarpeeksi_rahaa_veloitetaan_kortilta_summa_edullinen(
        self,
    ):
        self.kortin_saldo_oikein(
            self.kassapaate.syo_edullisesti_kortilla, self.kortti, 7.60
        )

    def test_korttimaksu_jos_kortilla_tarpeeksi_rahaa_veloitetaan_kortilta_summa_maukkaasti(
        self,
    ):
        self.kortin_saldo_oikein(
            self.kassapaate.syo_maukkaasti_kortilla, self.kortti, 6.00
        )

    def test_korttimaksu_jos_kortilla_ei_tarpeeksi_rahaa_saldo_ei_muutu_edullinen(
        self,
    ):
        self.kortin_saldo_oikein(
            self.kassapaate.syo_edullisesti_kortilla,
            self.kortti_liian_vahan_saldoa,
            1.00,
        )

    def test_korttimaksu_jos_kortilla_ei_tarpeeksi_rahaa_saldo_ei_muutu_maukkaasti(
        self,
    ):
        self.kortin_saldo_oikein(
            self.kassapaate.syo_maukkaasti_kortilla,
            self.kortti_liian_vahan_saldoa,
            1.00,
        )

    def test_korttimaksu_edullisesti_palauttaa_true_jos_saldo_riittaa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)

    def test_korttimaksu_maukkaasti_palauttaa_true_jos_saldo_riittaa(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)

    def test_korttimaksu_edullisesti_palauttaa_False_jos_saldo_ei_riita(self):
        self.assertEqual(
            self.kassapaate.syo_edullisesti_kortilla(self.kortti_liian_vahan_saldoa),
            False,
        )

    def test_korttimaksu_maukkaasti_palauttaa_False_jos_saldo_ei_riita(self):
        self.assertEqual(
            self.kassapaate.syo_maukkaasti_kortilla(self.kortti_liian_vahan_saldoa),
            False,
        )

    def test_korttimaksu_myytyjen_lounaiden_maara_kasvaa_edullisesti(self):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_edullisesti_kortilla, 1, "edulliset", self.kortti
        )

    def test_korttimaksu_myytyjen_lounaiden_maara_kasvaa_maukkaasti(self):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_maukkaasti_kortilla, 1, "maukkaat", self.kortti
        )

    def test_korttimaksu_myytyjen_lounaiden_maara_ei_kasva_jos_ei_saldoa_edullisesti(
        self,
    ):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_edullisesti_kortilla,
            0,
            "edulliset",
            self.kortti_liian_vahan_saldoa,
        )

    def test_korttimaksu_myytyjen_lounaiden_maara_ei_kasva_jos_ei_saldoa_maukkaasti(
        self,
    ):
        self.myytyjen_lounaiden_maara_oikein(
            self.kassapaate.syo_maukkaasti_kortilla,
            0,
            "maukkaat",
            self.kortti_liian_vahan_saldoa,
        )

    def test_lataa_rahaa_kortille_kassan_saldo_muuttuu(self):
        self.kassan_saldo_kasvaa(
            self.kassapaate.lataa_rahaa_kortille, 1000, 1010.0, self.kortti
        )

    def test_lataa_rahaa_kortille_kortin_saldo_muuttuu(self):
        self.kortin_saldo_oikein(
            self.kassapaate.lataa_rahaa_kortille, self.kortti, 20.00, 1000
        )

    def test_lataa_rahaa_kortille_negatiivisella_summalla_kassan_saldo_ei_muutu(self):
        self.kassan_saldo_kasvaa(
            self.kassapaate.lataa_rahaa_kortille, -100, 1000.0, self.kortti
        )

    def test_lataa_rahaa_kortille_negatiivisella_summalla_kortin_saldo_ei_muutu(self):
        self.kortin_saldo_oikein(
            self.kassapaate.lataa_rahaa_kortille, self.kortti, 10.00, -100
        )
