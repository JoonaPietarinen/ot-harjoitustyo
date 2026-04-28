# Changelog

## Viikko 3

- Pelaaja voi käynnistää pelin ja näkee päävalikon (uusi peli, tulokset, lopetus)
- Pelaaja näkee ruudukkokartan ja oman hahmonsa (@)
- Pelaaja voi liikkua neljään suuntaan (w, a, s, d)
- Pelaaja ei voi liikkua seinään tai kartan ulkopuolelle
- Pelaaja näkee elämäpisteet ja askelmäärän pelin aikana
- Pelaaja voi voittaa löytämällä uloskäynnin (X)
- Lisätty Player-luokka, joka sisältää pelaajan tilan (positio, hp, askeleet)
- Lisätty Game-luokka, joka vastaa pelilogiikasta ja liikkumisen validoinnista
- Lisätty ConsoleUI-luokka, joka vastaa tekstikäyttöliittymästä ja päävalikosta
- Toteutettu alustava paras tulos-seuranta pelin ajon aikana muistissa
- Testattu pelaajan liikkuminen, seiniin törmääminen, virheellisen syötteen käsittely sekä pelin voittaminen ja lopettaminen
- Yhteensopivuus Linuxille (termios/tty) ja Windowsille (msvcrt) näppäimen lukemiseen
- Myös invoke komennoissa huomioidaan Linux ja Windows.

## Viikko 4

- Luotu models hakemisto, johon sisällytetään mm. entityt (player, enemy)
- Lisätty yksinkertainen vihollinen
- Lisätty yksinkertainen taistelu systeemi
- Pelaaja luokkaan lisätty vahinko (damage) ja tapot
- Pelaaja voi nyt hävitä pelin kuollessaan

## Viikko 5

- Erotettu käyttöliittymätekstit sovelluslogiikasta `GameEvent`-enumin avulla
- Lisätty tulosten pysyvä tallennus tiedostoon (`data/scores.json`)
- Lisätty `ScoreRepository`, joka vastaa tulosten lukemisesta ja tallentamisesta
- Päävalikon "Tulokset" näyttää tallennetut top 10 tulosta
- Lisätty repositoryn automaattiset testit (`test_score_repository.py`)

## Viikko 6

- Lisätty potion-esineet ja keräysmekaniikka
- Pelaaja voi käyttää juoman komennolla `u`
- Lisätty `Potion`-malli ja potionien näkyminen kartalla
- Pelaajan tilaan lisättiin juomien määrä
- Lisätty testit potionien poimimiselle, käytölle ja juoman puuttumiselle
- Lisätty pygame-pohjainen käyttöliittymä tekstikäyttöliittymän rinnalle
- Pelaaja voi ohjata peliä ilman terminaalisyötettä pygame-ikkunassa
- Kartta, viholliset, potionit ja pelaajan tilastot piirretään graafisesti
- Päävalikko ja tulosnäkymä toteutettiin pygame-ikkunaan
- Muutoksia pelaajan ja vihollisten elämäpisteisiin
- Peli tallentaa nyt myös tappojen määrän
