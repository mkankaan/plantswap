# 🔄 PlantSwap 🪴

🌵 [Kuvaus](#kuvaus) <br/>
🌵 [Asennusohjeet (Linux/MacOS)](#asennusohjeet) <br/>
🌵 [Sovelluksen tila](#tila) <br/>
🌵 [Sovelluksen testaus](#testaus) <br/>

## <a name="kuvaus"></a> Kuvaus

- Käyttäjä pystyy lisäämään ilmoituksia huonekasveista, jotka haluaisi antaa vaihtoon.
- Sovelluksen tarkoitus on, että sen avulla voi vaihtaa kasveja tai pistokkaita muiden käyttäjien kanssa tai esimerkiksi löytää uuden kodin kasville, jota ei voi/halua pitää, ja saada vaihdossa toisen toivomansa kasvin.
- Käyttäjä pystyy luomaan tunnuksen, kirjautumaan sisään ja muokkaamaan profiiliaan. Profiili on näkyvillä myös muille käyttäjille. Profiilissa näkyy kaikki käyttäjän lisäämät ilmoitukset. Käyttäjä voi myös poistaa tilinsä.
- Käyttäjä näkee muiden lisäämät ilmoitukset ja pystyy etsimään ilmoituksia kasvin nimen ja sijainnin perusteella.
- Pääasiallinen tietokohde: ilmoitus. Toissijainen tietokohde: kommentti ilmoitukseen.
- Käyttäjä voi muokata ja poistaa omia ilmoituksiaan ja kommenttejaan.
- Ilmoituksen sivulla näkyy katselukertojen määrä.

## <a name="asennusohjeet"></a> Asennusohjeet (Linux/MacOS)

Seuraavat ohjeet on tarkoitettu sovelluksen asennukseen Linux- ja MacOS-käyttöjärjestelmillä. Muilla käyttöjärjestelmillä komennot ja sivuston osoite saattavat poiketa.

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

- Käyttäjä voi hakea ilmoituksia kasvin nimen ja/tai lähettäjän sijainnin perusteella.

### Tietoturva

- Kaikkien tietokohteiden luontiin, muokkaukseen ja poistamiseen liittyvät toiminnot vaativat sisäänkirjautumisen. Käyttäjältä on estetty muiden kuin hänen omien tietokohteidensa muokkaus ja poisto.
- csrf on käytössä kaikissa lomakkeissa, jotka vaativat sisäänkirjautumisen.

## <a name="testaus"></a> Sovelluksen testaus

### Ohjeet testaukseen

Sovelluksen tehokkuutta voi halutessaan testata ajamalla projektikansiossa komennon

```
python3 seed.py
```

Sovelluksen voi sen jälkeen käynnistää normaalisti komennolla 

```
flask run
```

seed.py-tiedosto sisältää skriptin, joka lisää tietokantaan 1000 käyttäjää, 100 000 listausta ja miljoona kommenttia. Aina kun sivu ladataan sovelluksen ollessa käynnissä, komentotulkkiin tulostuu lataukseen kulunut aika.

### Raportti

Sovelluksen toiminnan nopeuttamiseksi etusivulla on käytössä sivutus. Tietokantaan on myös lisätty kaksi indeksiä nopeuttamaan hakuja. Seuraavissa kuvissa on nähtävissä sovelluksen latausnopeus ilman näitä ominaisuuksia ja niiden kanssa. Ennen testausta tietokantaan on lisätty suuri määrä tietoa yllä kuvatun seed.py-tiedoston avulla.

#### Ei sivutusta, ei indeksiä

