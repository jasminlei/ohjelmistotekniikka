# Ohjelmistotekniikka, harjoitustyö

Tämä on Helsingin yliopiston _Ohjelmistotekniikka_-kurssin harjoitustyö.

## Opintojen seurantasovellus:

Harjoitustyön aiheena on opintojen seurantasovellus. Käyttäjä voi luoda opintosuunnitelman, aikatauluttaa kursseja, merkata kursseja suoritetuksi sekä seurata tilastoja opintojensa etenemisestä.

## Release

[Viikko 5](https://github.com/jasminlei/ohjelmistotekniikka/releases/tag/viikko5)

## Dokumentaatio

[Vaatimusmäärittely](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/vaatimusmaarittely.md)

[Työaikakirjanpito](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/tuntikirjanpito.md)

[Changelog](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/changelog.md)

[Arkkitehtuuri](https://github.com/jasminlei/ohjelmistotekniikka/blob/main/harjoitustyo/dokumentaatio/arkkitehtuuri.md)

## Asennus

1. Kloonaa projekti haluamaasi paikkaan komennolla:

```
git clone https://github.com/jasminlei/ohjelmistotekniikka
```

2. Siirry harjoitustyö-kansioon komennolla:

```
cd harjoitustyo
```

3. Asenna riippuvuudet komennolla:

```
poetry install
```

4. Alusta sovellus (luo tietokanta-tiedoston data-kansioon):

```
poetry run invoke build
```

5. Käynnistä sovellus komennolla:

```
poetry run invoke start
```

## Komentorivitoiminnot

- Sovelluksen käynnistys: `poetry run invoke start`

- Testien suoritus: `poetry run invoke tests`

- Testikattavuusraportin voi generoida (avautuu suoraan selaimeen): `poetry run invoke coverage-report`

- Pylintin voi suorittaa: `poetry run invoke pylint`

## Käyttöohjeet

- Ohjelma käynnistyy komennolla `poetry run invoke start`. Tämä avaa sovelluksen uudessa ikkunassa. Luo ensin käyttäjätunnus ja kirjaudu sisään, jonka jälkeen voit lisätä kursseja tai luoda opintosuunnitelman.
