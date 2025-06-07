# 🔄 PlantSwap 🪴

### (Jatkan edellisellä toteutuksella kesken jäänyttä projektia)

🌵 [Kuvaus](#kuvaus) <br/>
🌵 [Ajo-ohjeet](#ajo-ohjeet)

## <a name="kuvaus"></a> Kuvaus

- Käyttäjä pystyy lisäämään ilmoituksia huonekasveista, jotka haluaisi antaa vaihtoon.
- Käyttäjä pystyy luomaan toivelistan kasveista, joita haluaisi vastaanottaa vaihdossa.
- Sovelluksen tarkoitus on, että sen avulla voi vaihtaa kasvien pistokkaita muiden käyttäjien kanssa tai esimerkiksi löytää uuden kodin kasville, jota ei voi/halua pitää, ja saada vaihdossa toisen toivomansa kasvin. Sovellus ehdottaa käyttäjälle toisia käyttäjiä, joiden toiveet, tarjonta ja sijainti ovat yhteensopivia omien kanssa.
- Käyttäjä pystyy luomaan tunnuksen, kirjautumaan sisään ja muokkaamaan profiiliaan. Profiili on näkyvillä myös muille käyttäjille. Profiilissa näkyy kaikki käyttäjän lisäämät ilmoitukset. Käyttäjä voi myös poistaa tilinsä.
- Käyttäjä näkee muiden lisäämät ilmoitukset ja pystyy suodattamaan ilmoituksia sijainnin perusteella (mahdollisesti myös muita luokitteluja). Käyttäjä pystyy myös hakemaan ilmoituksia kasvin nimen perusteella.
- Pääasiallinen tietokohde: ilmoitus. Toissijaiset tietokohteet: toivelista ja kommentti ilmoitukseen.
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
