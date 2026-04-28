# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen tarkoituksena on *pieni*, **laajennettavissa** oleva roguelike-tyyppinen luolastoseikkailupeli, jossa pelaaja liikkuu ruudukkopohjaisessa luolastossa, taistelee vihollisia vastaan, kerää esineitä ja pyrkii selviytymään mahdollisimman pitkälle ennen kuolemaansa.  
Tavoitteena on toteuttaa selkeästi rajattu perusversio, jonka keskeiset toiminnot saadaan nopeasti valmiiksi ja jonka ympärille voidaan lisätä uusia pelimekaniikkoja, pysyväistallennus ja testattava sovelluslogiikka.

## Käyttäjät

Sovelluksessa on vain yksi käyttäjärooli: pelaaja, joka käynnistää pelin, ohjaa hahmoa ja tarkastelee pelin esittämiä tuloksia (esimerkiksi pisteitä tai tilastoja).

## Käyttöliittymäluonnos

**Alkuvaiheessa** sovellus tarjoaa yksinkertaisen tekstipohjaisen käyttöliittymän, jossa pelaaja näkee ruudukkokartan, oman hahmonsa, viholliset ja perusstatistiikat.  
Pelin käynnistyttyä pelaajalle näytetään päävalikko, josta voi aloittaa uuden pelin, tarkastella aiempien pelien tuloksia tai lopettaa sovelluksen.

## Perusversion tarjoama toiminnallisuus

### Pelin aloitus ja perusnäkymä

- Pelaaja voi käynnistää sovelluksen ja siirtyä päävalikkoon.  – tehty
- Pelaaja voi aloittaa uuden pelin päävalikosta.  – tehty
- Uusi peli käynnistyy ennalta määritellystä luolastosta, jossa on seinistä ja lattiasta koostuva ruudukkokartta.  – tehty
- Pelaaja näkee kartan lisäksi oman hahmonsa elämäpisteet ja mahdolliset perustilastot (esim. taso tai tappojen määrä).  – tehty

### Liikkuminen ja ympäristö

- Pelaaja voi liikkua neljään suuntaan (ylös, alas, vasen, oikea).  – tehty
- Liikkuminen ei onnistu seinäruutuihin tai kartan ulkopuolelle.  – tehty
- Kartalla voi olla erilaisia ruututyyppejä (esim. lattia, seinä, uloskäynti), jotka vaikuttavat liikkumiseen.  – tehty

### Viholliset ja taistelu

- Kartalla on vähintään yksi vihollistyyppi, joka näkyy pelaajalle ruudulla.  – tehty
- Viholliset toimivat vuoropohjaisesti: aina pelaajan vuoron jälkeen on vihollisten vuoro.  – tehty
- Kun pelaaja liikkuu vihollisen ruutuun tai hyökkää sen viereen, käynnistyy yksinkertainen taistelumekaniikka (esim. hyökkäys, vihollisen vastahyökkäys).  – tehty
- Jos pelaajan elämäpisteet laskevat nollaan, peli päättyy häviöön.  – tehty

### Esineet

- Kartalla voi olla perusesineitä (esim. parantavia potion-juomia).  – tehty
- Pelaaja voi kerätä esineitä ja käyttää niitä (esim. potion palauttaa osan elämäpisteistä).  – tehty

### Pelin päättyminen ja tulos

- Peli päättyy, kun pelaaja kuolee tai saavuttaa tason uloskäynnin.  – tehty
- Peli laskee yksinkertaisen pistemäärän (esim. kuljetut askeleet, tapetut viholliset, kerätyt esineet).  – tehty
- Peli näyttää lopputuloksen yhteenvedon (esim. pistemäärä ja muut olennaiset tilastot).  – tehty

### Tietojen tallennus

- Sovellus tallentaa perusversiossa ainakin yhden tyyppisen pysyvän tiedon tiedostoon (esim. paras pistetulos tai lista parhaista tuloksista).  – tehty
- Pelaaja voi päävalikosta tarkastella aiempia tallennettuja tuloksia.  – tehty

## Jatkokehitysideoita

Perusversion jälkeen sovellusta voidaan laajentaa ajan salliessa esimerkiksi seuraavilla toiminnallisuuksilla:

- Useampi vaikeustaso, joka vaikuttaa vihollisten määrään, vahinkoon tai kartan kokoon.  
- Useampia vihollistyyppejä erilaisilla ominaisuuksilla (esim. liikkumislogiikka, hyökkäysvoima, erikoiskyvyt).  
- Laajempi esine- ja inventaariomekaniikka, jossa pelaaja voi kantaa useita esineitä, aseita ja panssareita.  
- Satunnaisesti generoitavat luolastot, jotka luodaan algoritmisesti pelin käynnistyessä tai luetaan konfiguraatiotiedostoista.  
- Mahdollisuus jatkaa aiemmin tallennettua peliä useamman tallennus-slotin avulla.  
- Graafinen käyttöliittymä tekstipohjaisen käyttöliittymän rinnalle tai tilalle. – tehty
