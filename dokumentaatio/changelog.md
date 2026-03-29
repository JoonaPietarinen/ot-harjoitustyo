# Changelog

## Viikko 3

- Pelaaja voi käynnistää pelin ja näkee päävalikon (uusi peli, tulokset, lopetus)
- Pelaaja näkee ruudukkokartan ja oman hahmonsa (@)
- Pelaaja voi liikkua neljään suuntaan (w, a, s, d)
- Pelaaja ei voi liikkua seinään tai kartan ulkopuolelle
- Pelaaja näkee elämäpisteet ja askelmäärän pelin aikana
- Pelaaja voi voittaa löytämällä uloskäynnin (E)
- Lisätty Player-luokka, joka sisältää pelaajan tilan (positio, hp, askeleet)
- Lisätty Game-luokka, joka vastaa pelilogiikasta ja liikkumisen validoinnista
- Lisätty ConsoleUI-luokka, joka vastaa tekstikäyttöliittymästä ja päävalikosta
- Toteutettu alustava paras tulos-seuranta pelin ajon aikana muistissa
- Testattu pelaajan liikkuminen, seiniin törmääminen, virheellisen syötteen käsittely sekä pelin voittaminen ja lopettaminen
- Yhteensopivuus Linuxille (termios/tty) ja Windowsille (msvcrt) näppäimen lukemiseen
- Myös ivoke komennoissa huomioidaan Linux ja Windows.
