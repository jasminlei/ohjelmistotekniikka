# Sovelluksen käyttöohje

Lataa projektin uusimman releasen lähdekoodi valitsemalla Assets-osion alta Source code.

## Ohjelman käynnistäminen

Siirry harjoitustyö-kansioon:

```
cd harjoitustyo
```

Asenna riippuvuudet:

```
poetry install
```

Alusta sovelluksen tietokanta:

```
poetry run invoke build
```

Käynnistä sovellus:

```
poetry run invoke start
```

## Rekisteröityminen ja kirjautuminen

Rekisteröidy ensin painamalla "Rekisteröidy" -nappia. Tämän jälkeen voit kirjautua sisään painamalla "Kirjaudu sisään"-nappia ja syöttämällä oikean käyttäjätunnuksen ja salasanan.

## Kirjautumisen jälkeen

### Lisää kurssi

Voit lisätä sovellukseen kurssin painamalla "Lisää kurssi" -nappia. Syötä kurssin koodi (esim. TKT101), kurssin nimi (esim. Ohjelmistotekniikka), opintopisteet (esim. 5) sekä halutessasi kuvaus (esim. Hauska kurssi jossa tehdään harjoitustyönä sovellus). Paina vihreää "Lisää kurssi" -nappia. Jos joku meni pieleen, sivulle ilmestyy virheilmoitus punaisella tekstillä, jos ei, niin vihreällä tekstillä ilmestyy "Kurssi Ohjelmistotuotanto lisätty".

### Tarkastele lisättyjä kursseja

Järjestelmään lisätyt kurssit löytyvät painamalla "Listaa kurssit" -nappia. Voit valita kurssin painamalla kurssin nimeä, jolloin kurssista aukeaa lisätietoja. Kun olet valinnut kurssin, voit lisätä kurssin suoritetuksi painamalla vihreää "Merkitse suoritetuksi" -nappia ja syöttämällä aukeavaan ikkunaan suorituspäivämäärän ja valitsemalla arvosanan. Voit poistaa kurssin painamalla punaista poista kurssi -nappia.

### Luo opintosuunnitelma

Voit luoda opintosuunnitelman klikkamalla päänäkymässä vihreää "Lisää opintosuunnitelma" -nappia. Anna opintosuunnitelmalle nimi "esim. Ensisijainen TKT opintosuunnitelma" ja tavoite opintopistemäärä (esim. 180), ja paina "Tallenna" -nappia.

### Tarkastele opintosuunnitelmia ja lisää suunnitelmaan vuosia ja kursseja

Klikkaa sovelluksen päänäkymästä "Tarkastele opintosuunnitelmia" -nappia. Valitse haluamasi opintosuunnitelma.

Lisää suunnitelmaan vuosi klikkaamalla "Lisää akateeminen vuosi" -nappia. Lisää haluamasi vuodet (esim. 2024-2025 tarkoittaa vuotta alkaen syksystä 2024 päättyen vuoteen 2025). Ylös ilmestyy valikko, josta voit valita lisäämäsi vuoden. Voit myös lisätä enemmän vuosia halutessasi.

Valitse haluamasi vuosi, ja alapuolelle aukeaa näkymä opintosuunnitelmasta. Voit navigoida eri periodien välillä klikkaamalla periodin nimeä.

Voit lisätä tallentamiasi kursseja opintosuunnitelmaan tietylle periodille klikkaamalla "Lisää kurssi" -nappia. Klikattuasi aukeaa lista kursseista, jotka olet lisännyt järjestelmään. Jos kurssia ei ole vielä suunnitelmassa, sen nimen vieressä on lisää-nappi, jota painamalla se siirtyy suunnitelmaan.

Jos klikkaat kurssin nimeä suunnitelmassa, aukeaa ikkuna, jossa voit joko lisätä kurssin suoritetuksi, muokata suoritusta tai poistaa kurssin suunnitelmasta. Kurssin poistaminen suunnitelmasta ei poista sitä järjestelmästä, eli voit lisätä sen uudestaan esim. toiselle periodille halutessasi.

Voit myös poistaa vuoden, klikkaamalla "poista vuosi" -nappia.

### Tilastojen tarkastelu

Klikkaa sovelluksen päänäkymässä "Tilastot" -nappia. Valitse haluamasi opintosuunnitelma, ja tarkastele tilastoja opintojen etenemisestä.

### Uloskirjautumienn

Paina sovelluksen päänäkymässä punaista "Kirjaudu ulos" -nappia.
