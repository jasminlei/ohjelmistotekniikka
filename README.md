# Ohjelmistotekniikka, harjoitustyö

Tämä on Helsingin yliopiston _Ohjelmistotekniikka_-kurssin harjoitustyö.

## Opintojen seurantasovellus:

Harjoitustyön aiheena on opintojen seurantasovellus. Käyttäjä voi luoda opintosuunnitelman, aikatauluttaa kursseja, merkata kursseja suoritetuksi sekä seurata tilastoja opintojensa etenemisestä.

## Dokumentaatio

[Vaatimusmäärittely](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/vaatimusmaarittely.md)

[Työaikakirjanpito](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/tuntikirjanpito.md)

[Changelog](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/changelog.md)

## Asennus

1. Asenna riippuvuudet komennolla:

```
poetry install
```

2. Alusta sovellus (luo tietokanta-tiedoston data-kansioon):

```
poetry run invoke build
```

3. Käynnistä sovellus komennolla:

```
poetry run invoke start
```

## Komentorivitoiminnot

- Sovelluksen käynnistys: `poetry run invoke start`

- Testien suoritus: `poetry run invoke test`

- Testikattavuusraportin voi generoida (avautuu suoraan selaimeen): `poetry run invoke coverage_report`

## Käyttöohjeet

- Ohjelma käynnistyy komennolla `poetry run invoke start`, ja terminaaliin tulostuu kaikki tämänhetkiset käytössä olevat toiminnot ja pikanäppäimet niiden käyttämiseen.
