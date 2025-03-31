\*\*Huomio sovelluksen ajamisesta: GitHubissa ei ole config.py eikä database.db -tiedostoja, ne täytyy itse lisätä ja ajaa komento ```sqlite3 database.db < schema.sql``` jotta sovelluksen saa käyntiin\*\*

# 🔄 PlantSwap 🪴

- Käyttäjä pystyy lisäämään ilmoituksia huonekasveista, jotka haluaisi antaa vaihtoon.
- Käyttäjä pystyy luomaan toivelistan kasveista, joita haluaisi vastaanottaa vaihdossa.
- Sovelluksen tarkoitus on, että sen avulla voi vaihtaa kasvien pistokkaita muiden käyttäjien kanssa tai esimerkiksi löytää uuden kodin kasville, jota ei voi/halua pitää, ja saada vaihdossa toisen toivomansa kasvin. Sovellus ehdottaa käyttäjälle toisia käyttäjiä, joiden toiveet, tarjonta ja sijainti ovat yhteensopivia omien kanssa.
- Käyttäjä pystyy luomaan tunnuksen, kirjautumaan sisään ja muokkaamaan profiiliaan. Profiili on näkyvillä myös muille käyttäjille. Profiilissa näkyy kaikki käyttäjän lisäämät ilmoitukset. Käyttäjä voi myös poistaa tilinsä.
- Käyttäjä näkee muiden lisäämät ilmoitukset ja pystyy suodattamaan ilmoituksia sijainnin ja kasvin suvun perusteella (mahdollisesti myös muita luokitteluja). Käyttäjä pystyy myös hakemaan ilmoituksia kasvin nimen (yleisnimen tai latinalaisen) perusteella.
- Käyttäjä voi muokata ja poistaa omia ilmoituksiaan ja kommenttejaan. Käyttäjä voi myös lisätä muiden ilmoituksia suosikkeihin.
- Pääasiallinen tietokohde: ilmoitus. Toissijaiset tietokohteet: toivelista ja kommentti ilmoitukseen.
- Sovellus näyttää tilastoja siitä, kuinka monta kertaa ilmoitusta on katseltu ja kuinka monta kertaa se on lisätty suosikkeihin.

## 🌵 Toteutetut ominaisuudet

Päivitetty 30.3.2025

### Kirjautuminen ja profiili

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään
- Käyttäjä voi vaihtaa profiilikuvansa
- Käyttäjä näkee muiden käyttäjien profiilit
- Profiilissa näkyy lista käyttäjän luomista ilmoituksista
- Käyttäjä voi poistaa profiilinsa. Profiili ei katoa tietokannasta, vaan sen status muuttuu

### Ilmoitukset

- Käyttäjä voi lisätä, muokata ja poistaa ilmoituksia. Ilmoitus poistuu tietokannasta pysyvästi
- Käyttäjä voi vaihtaa kuvan ilmoitukseen
- Jokaisen ilmoituksen voi klikata auki omalle sivulleen, jossa näkyy kaikki siihen liittyvät tiedot, lisäyspäivä, katselukerrat ja kommentit (ei toteutettu vielä)

### Haku

- Käyttäjä voi hakea ilmoituksia kaavin nimen perusteella. Ilman hakusanaa hakusivu näyttää oletusarvoisesti kaikki ilmoitukset tietokannassa. Tarkoituksena lisätä enemmän hakusanoja ja suodattimia

Kaikkien tietokohteiden luontiin, muokkaukseen ja poistamiseen liittyvät toiminnot vaativat sisäänkirjautumisen. Muokkaus ja poisto vaativat lisäksi käyttäjän id:n tarkistuksen.
