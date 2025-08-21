# 🔄 PlantSwap 🪴

🌵 [Kuvaus](#kuvaus) <br/>
🌵 [Ajo-ohjeet](#ajo-ohjeet) <br/>
🌵 [Sovelluksen tila](#tila) <br/>
🌵 [Testaus suurella tietomäärällä](#testaus) <br/>

## <a name="kuvaus"></a> Kuvaus

- Käyttäjä pystyy lisäämään ilmoituksia huonekasveista, jotka haluaisi antaa vaihtoon.
- Sovelluksen tarkoitus on, että sen avulla voi vaihtaa kasveja tai pistokkaita muiden käyttäjien kanssa tai esimerkiksi löytää uuden kodin kasville, jota ei voi/halua pitää, ja saada vaihdossa toisen toivomansa kasvin.
- Käyttäjä pystyy luomaan tunnuksen, kirjautumaan sisään ja muokkaamaan profiiliaan. Profiili on näkyvillä myös muille käyttäjille. Profiilissa näkyy kaikki käyttäjän lisäämät ilmoitukset. Käyttäjä voi myös poistaa tilinsä.
- Käyttäjä näkee muiden lisäämät ilmoitukset ja pystyy etsimään ilmoituksia kasvin nimen ja sijainnin perusteella.
- Pääasiallinen tietokohde: ilmoitus. Toissijainen tietokohde: kommentti ilmoitukseen.
- Käyttäjä voi muokata ja poistaa omia ilmoituksiaan ja kommenttejaan.
- Ilmoituksen sivulla näkyy katselukertojen määrä.

## <a name="ajo-ohjeet"></a> Ajo-ohjeet (Linux)

Suorita seuraavat komennot projektikansiossa.

Alusta tietokanta:

```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
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

Sovellus käynnistyy oletusarvoisesti osoitteeseen http://127.0.0.1:5000

## <a name="tila"></a> Sovelluksen tila

### Kirjautuminen ja profiili

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään.
- Käyttäjä voi vaihtaa ja poistaa profiilikuvansa.
- Käyttäjä näkee muiden käyttäjien profiilit.
- Profiilissa näkyy lista käyttäjän luomista ilmoituksista.
- Käyttäjä voi poistaa profiilinsa. Profiili ei katoa tietokannasta, vaan sen status muuttuu.

### Ilmoitukset (pääasiallinen tietokohde)

- Käyttäjä voi lisätä, muokata ja poistaa ilmoituksia. Ilmoitus poistuu tietokannasta pysyvästi.
- Käyttäjä voi vaihtaa ja poistaa ilmoituksen kuvan.
- Kasville voi lisätä luokitteluja: tyyppi (pistokas/kokonainen kasvi) ja valon tarve (vähäinen/keskitaso/runsas). Luokkia voi päivittää jälkeenpäin.
- Jokaisen ilmoituksen voi klikata auki omalle sivulleen, jossa näkyy siihen liittyvät tiedot: lisäyspäivä, luokat, katselukerrat ja kommentit.

### Kommentit (toissijainen tietokohde)

- Käyttäjä voi lisätä kommentin ilmoitukseen.
- Käyttäjä pystyy muokkaamaan ja poistamaan omia kommenttejaan. Kommentti poistuu tietokannasta pysyvästi.

### Haku

- Käyttäjä voi hakea ilmoituksia kasvin nimen ja/tai lähettäjän sijainnin perusteella. Ilman hakutermejä hakusivu näyttää oletusarvoisesti kaikki ilmoitukset tietokannassa.

### Tietoturva

- Kaikkien tietokohteiden luontiin, muokkaukseen ja poistamiseen liittyvät toiminnot vaativat sisäänkirjautumisen. Muokkaus ja poisto vaativat lisäksi käyttäjän id:n tarkistuksen.
- csrf on käytössä kaikissa lomakkeissa, jotka vaativat sisäänkirjautumisen.

## <a name="testaus"></a> Testaus suurella tietomäärällä
