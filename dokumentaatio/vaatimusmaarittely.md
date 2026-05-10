# Vaatimusmäärittely

## Sovelluksen tarkoitus

Yksinkertainen roguelike-tyyppinen luolastoseikkailupeli, jossa pelaaja liikkuu ruudukkopohjaisessa luolastossa, taistelee vihollisia vastaan, kerää esineitä ja pyrkii selviytymään uloskäyntiin saakka.

## Käyttäjät

Sovelluksella on yksi käyttäjärooli: pelaaja.

## Käyttöliittymäluonnos

Sovellus tarjoaa kaksi käyttöliittymää:
- Tekstipohjainen käyttöliittymä
- Graafinen Pygame-pohjainen käyttöliittymä

Molempien kautta pelaaja pääsee päävalikkoon, josta voi aloittaa pelin, katsella tuloksia tai lopettaa sovelluksen.

## Perusversion tarjoama toiminnallisuus

### Pelin alussa

- Pelaaja voi valita vaikeustason (helppo, normaali, vaikea)
- Jokainen vaikeustaso käyttää eri karttaa ja vihollisten määrää
- Pelaaja näkee ruudukkokartan, omat tilastot (HP, askeleet, tapot, juomat)

### Pelinaikana

- Pelaaja voi liikkua neljään suuntaan (W/A/S/D)
- Pelaaja voi käyttää juomaa (U) paranatakseen elämäpisteitä
- Pelaaja voi lopettaa pelin (Q)
- Pelaaja taistelee vihollisia vastaan
- Pelaaja saa elämää takaisin tappamalla vihollisia (life steal)
- Pelaaja voi kerätä juomia kartalta

### Pelin päätyttyä

- Peli päättyy pelaajan kuollessa tai saavutettaessa uloskäynnin
- Pelaaja näkee tulokset (askeleet, tapot, vaikeustaso)
- Tulokset tallentuvat JSON-tiedostoon

### Tulosten tarkastelu

- Pelaaja voi tarkastella kaikkia tuloksia (Top 10)
- Pelaaja voi filteroida tuloksia vaikeustason mukaan
- Jokaisen vaikeustason omat leaderboardit


## Jatkokehitysideoita

- Satunnaisesti generoitavat luolastot
- Pelitilan tallentaminen ja lataaminen
- Erilaisia esineitä ja aseita
- Erikoiskyvyt vihollisille
- Kehitysjärjestelmä pelaajalle
- Ääniefektit ja musiikki
- Useampia tasoja ja teemoja
- Kehittyneempi taistelusysteemi (esim. vuoropohjainen omalla käyttöliittymällä)
