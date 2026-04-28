# Käyttöohje

## Asennus ja käynnistys

### Edellytykset
- Python 3.12+
- Poetry (Python-riippuvuuksien hallintaan)

### Asennus
Palautusrepositoriosta:

```bash
cd ot-harjoitustyo
poetry install
```

### Käynnistys


```bash
poetry run invoke start
```


## Peli-ohjaus

Peli käyttää näppäinohjausta:

| Näppäin | Toiminto |
|---------|----------|
| **W**   | Liiku ylös |
| **A**   | Liiku vasemmalle |
| **S**   | Liiku alas |
| **D**   | Liiku oikealle |
| **U**   | Käytä juoman (potion) |
| **Q**   | Lopeta peli tai palaa valikkoon |
| **Enter / Esc** | Valinnan tekeminen valikossa |

## Pelin näkymät

### Päävalikko

Avautuu pelin käynnistyessä. Valinnat:

- **1**: Aloita uusi peli
- **2**: Näytä tallennetut tulokset
- **3**: Lopeta sovellus

### Pelinäkymä

```
- Kartta: Ruudukkomuotoinen ympäristö
  - @  = pelaajasi
  - E  = vihollinen
  - !  = potion (juoma)
  - X  = uloskäynti (voitto)
  - #  = seinä (ei voi mennä läpi)
  - .  = lattia (voi liikkua)

- HUD (näytön alaosa):
  - HP: Elämäpisteet
  - Askeleet: Kuinka monta ruutua olet käynyt
  - Tapot: Kuinka monta vihollista olet tappanut
  - Juomat: Potionien määrä inventaariossasi
```

### Tulosnäkymä

Näyttää top 10 parasta tulosta järjestettynä:
1. Vähin askelmäärä
2. Saman askelmäärän sisällä: eniten tappoja

## Pelimekaniikka

### Liikkuminen
- Liiku ruudukkoilla
- Et voi mennä seinän läpi
- Kartan ulkopuolelle ei voi mennä

### Taistelu
- Kun liikut vihollisen viereen, taistelu "käynnistyy"
- Jos liikkuminen oli vihollisen suuntaan, vihollinen ottaa 1 vahinkoa
- Vihollinen hyökkää takaisin, jos on vielä elossa, ja pelaaja ottaa vahinkoa
- Jos taas liikkuminen ei ollut vihollisen suuntaan, vihollinen hyökkää
- Pelaaja voi hyökätä uudelleen liikkumalla uudestaan vihollisen suuntaan

### Esineet
- **Potion** (!) palauttaa 4 HP:tä kun käytetään
- Voit kantaa rajatonta määrää potioneja
- Poimi potion liikkumalla sen päälle

### Voittaminen / Häviäminen

**Voittaminen:**
- Liiku uloskäyntiin (X)
- Peli näyttää tuloksesi ja tallentaa sen

**Häviäminen:**
- Elämäpisteesi tippuvat nollaan taistelussa
- Peli päättyy, tulosta ei tallenneta

## Testaus

Testien suorittaminen:
```bash
poetry run invoke test
```

Testikattavuusraportin luonti:
```bash
poetry run invoke coverage-report
```
Raportti löytyy `htmlcov/`-hakemistosta.

## Koodin laatu

Pylint-tarkistus:
```bash
poetry run invoke lint
```

## Vianetsintä

### Pygame ei käynnisty
- Varmista, että `poetry install` on suoritettu
- Jos saat virheilmoituksen `- Installing pygame (2.6.1): Failed`, kokeile `poetry env use python3.12`, ja `poetry install` uudestaan
- Kokeile: `poetry run invoke start`
- Jos edelleen ongelmia, sovellus käyttää tekstikäyttöliittymää automaattisesti

### Tulokset eivät tallennu
- Tarkista, että hakemistolla `data/` on kirjoitusoikeudet
- Tiedosto luodaan automaattisesti ensimmäisen voiton jälkeen

### Peli "jumittuu"
- Q-näppäimellä voit poistua pelistä milloin tahansa
- Palaa päävalikkoon ja aloita uusi peli
