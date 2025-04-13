# 🔄 PlantSwap 🪴

- [Kuvaus](#kuvaus)
- [Ajo-ohjeet](#ajo-ohjeet)
- [Välipalautus 2](#palautus2)
- [Välipalautus 3](#palautus3)

## <a name="kuvaus"></a> Kuvaus

- Käyttäjä pystyy lisäämään ilmoituksia huonekasveista, jotka haluaisi antaa vaihtoon.
- Käyttäjä pystyy luomaan toivelistan kasveista, joita haluaisi vastaanottaa vaihdossa.
- Sovelluksen tarkoitus on, että sen avulla voi vaihtaa kasvien pistokkaita muiden käyttäjien kanssa tai esimerkiksi löytää uuden kodin kasville, jota ei voi/halua pitää, ja saada vaihdossa toisen toivomansa kasvin. Sovellus ehdottaa käyttäjälle toisia käyttäjiä, joiden toiveet, tarjonta ja sijainti ovat yhteensopivia omien kanssa.
- Käyttäjä pystyy luomaan tunnuksen, kirjautumaan sisään ja muokkaamaan profiiliaan. Profiili on näkyvillä myös muille käyttäjille. Profiilissa näkyy kaikki käyttäjän lisäämät ilmoitukset. Käyttäjä voi myös poistaa tilinsä.
- Käyttäjä näkee muiden lisäämät ilmoitukset ja pystyy suodattamaan ilmoituksia sijainnin ja kasvin suvun perusteella (mahdollisesti myös muita luokitteluja). Käyttäjä pystyy myös hakemaan ilmoituksia kasvin nimen (yleisnimen tai latinalaisen) perusteella.
- Käyttäjä voi muokata ja poistaa omia ilmoituksiaan ja kommenttejaan. Käyttäjä voi myös lisätä muiden ilmoituksia suosikkeihin.
- Pääasiallinen tietokohde: ilmoitus. Toissijaiset tietokohteet: toivelista ja kommentti ilmoitukseen.
- Sovellus näyttää tilastoja siitä, kuinka monta kertaa ilmoitusta on katseltu ja kuinka monta kertaa se on lisätty suosikkeihin.

## <a name="ajo-ohjeet"></a> Ajo-ohjeet

Suorita seuraavat komennot projektikansiossa.

Alusta tietokanta:

```
echo schema.sql > database.db
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

## <a name="palautus2"></a> Välipalautus 2

### Kirjautuminen ja profiili

- Käyttäjä voi luoda tunnuksen ja kirjautua sisään
- Käyttäjä voi vaihtaa profiilikuvansa
- Käyttäjä näkee muiden käyttäjien profiilit
- Profiilissa näkyy lista käyttäjän luomista ilmoituksista
- Käyttäjä voi poistaa profiilinsa. Profiili ei katoa tietokannasta, vaan sen status muuttuu

### Ilmoitukset (pääasiallinen tietokohde)

- Käyttäjä voi lisätä, muokata ja poistaa ilmoituksia. Ilmoitus poistuu tietokannasta pysyvästi
- Käyttäjä voi vaihtaa kuvan ilmoitukseen
- Jokaisen ilmoituksen voi klikata auki omalle sivulleen, jossa näkyy kaikki siihen liittyvät tiedot, lisäyspäivä, katselukerrat ja kommentit (ei toteutettu vielä)

### Haku

- Käyttäjä voi hakea ilmoituksia kaavin nimen perusteella. Ilman hakusanaa hakusivu näyttää oletusarvoisesti kaikki ilmoitukset tietokannassa. Tarkoituksena lisätä enemmän hakusanoja ja suodattimia

Kaikkien tietokohteiden luontiin, muokkaukseen ja poistamiseen liittyvät toiminnot vaativat sisäänkirjautumisen. Muokkaus ja poisto vaativat lisäksi käyttäjän id:n tarkistuksen.

## <a name="palautus3"></a> Välipalautus 3

### Kommentit (toissijainen tietokohde)

- Käyttäjä voi lisätä kommentin ilmoitukseen. Käyttäjä pystyy muokkaamaan ja poistamaan omia kommenttejaan

### Muuta

- csrf on käytössä kaikissa lomakkeissa, jotka vaativat sisäänkirjautumisen
