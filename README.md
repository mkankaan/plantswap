# 🔄 PlantSwap 🪴

🌵 [Kuvaus](#kuvaus) <br/>
🌵 [Ajo-ohjeet](#ajo-ohjeet) <br/>
🌵 [Välipalautus 3](#palautus3) <br/>

## <a name="kuvaus"></a> Kuvaus

- Käyttäjä pystyy lisäämään ilmoituksia huonekasveista, jotka haluaisi antaa vaihtoon.
- Sovelluksen tarkoitus on, että sen avulla voi vaihtaa kasveja tai pistokkaita muiden käyttäjien kanssa tai esimerkiksi löytää uuden kodin kasville, jota ei voi/halua pitää, ja saada vaihdossa toisen toivomansa kasvin.
- Käyttäjä pystyy luomaan tunnuksen, kirjautumaan sisään ja muokkaamaan profiiliaan. Profiili on näkyvillä myös muille käyttäjille. Profiilissa näkyy kaikki käyttäjän lisäämät ilmoitukset. Käyttäjä voi myös poistaa tilinsä.
- Käyttäjä näkee muiden lisäämät ilmoitukset ja pystyy suodattamaan ilmoituksia sijainnin perusteella (mahdollisesti myös muita luokitteluja). Käyttäjä pystyy myös hakemaan ilmoituksia kasvin nimen perusteella.
- Pääasiallinen tietokohde: ilmoitus. Toissijainen tietokohde: kommentti ilmoitukseen.
- Käyttäjä voi muokata ja poistaa omia ilmoituksiaan ja kommenttejaan. Käyttäjä voi myös lisätä muiden ilmoituksia suosikkeihin.
- Sovellus näyttää tilastoja siitä, kuinka monta kertaa ilmoitusta on katseltu ja kuinka monta kertaa se on lisätty suosikkeihin.

## <a name="ajo-ohjeet"></a> Ajo-ohjeet

Suorita seuraavat komennot projektikansiossa.

Alusta tietokanta:

```
sqlite3 database.db < schema.sql
```

Asenna Pythonin virtuaaliympäristö ja Flask:

```
python3 -m venv venv
source venv/bin/activate
pip install flask
```

Käynnistä sovellus komennolla

```
flask run
```

Sovellus käynnistyy oletusarvoisesti osoitteeseen http://localhost:5000

## <a name="palautus3"></a> Välipalautus 3

### Kirjautuminen ja profiili

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään.
- Käyttäjä voi vaihtaa profiilikuvansa.
- Käyttäjä näkee muiden käyttäjien profiilit.
- Profiilissa näkyy lista käyttäjän luomista ilmoituksista.
- Käyttäjä voi poistaa profiilinsa. Profiili ei katoa tietokannasta, vaan sen status muuttuu.

### Ilmoitukset (pääasiallinen tietokohde)

- Käyttäjä voi lisätä, muokata ja poistaa ilmoituksia. Ilmoitus poistuu tietokannasta pysyvästi.
- Käyttäjä voi vaihtaa kuvan ilmoitukseen.
- Jokaisen ilmoituksen voi klikata auki omalle sivulleen, jossa näkyy kaikki siihen liittyvät tiedot, lisäyspäivä, katselukerrat ja kommentit.
- Kasville voi lisätä luokittelun (pistokas). Tieto on tallennettu tietokannassa sarakkeeseen 'cutting' taulussa 'listings' (ei erillistä taulua). Tarkoituksena on, että ilmoituksia voi suodattaa luokittelun perusteella (ei toteutettu vielä).

### Kommentit (toissijainen tietokohde)

- Käyttäjä voi lisätä kommentin ilmoitukseen. Käyttäjä pystyy muokkaamaan ja poistamaan omia kommenttejaan.

### Haku

- Käyttäjä voi hakea ilmoituksia kasvin nimen perusteella. Ilman hakusanaa hakusivu näyttää oletusarvoisesti kaikki ilmoitukset tietokannassa. Tarkoituksena lisätä hakuun suodattimia.

### Tietoturva

- Kaikkien tietokohteiden luontiin, muokkaukseen ja poistamiseen liittyvät toiminnot vaativat sisäänkirjautumisen. Muokkaus ja poisto vaativat lisäksi käyttäjän id:n tarkistuksen.
- csrf on käytössä kaikissa lomakkeissa, jotka vaativat sisäänkirjautumisen.


