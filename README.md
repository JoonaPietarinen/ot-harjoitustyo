# Ohjelmistotekniikka, harjoitustyö

Yksinkertainen roguelike-tyyppinen luolastoseikkailupeli, jossa pelaaja yrittää läpäistä vihollisia ja potioneita sisältävän tason saavuttamalla uloskäynnin.

Pelaajan onnistuneista suorituksista tallennetaan tiedot käytetyistä askelista, tappojen määrästä sekä vaikeustasosta. Näitä tietoja voi tarkastella päävalikosta. Suorituksia voi olla tallennettuna yhteensä maksimissaan 20, mutta niistä näytetään max 10 per kategoria päävalikossa.

Peli toimii sekä Windows- että Linux-ympäristöissä.

## Dokumentaatio

- [Käyttöohje](dokumentaatio/kayttoohje.md)

- [Määrittelydokumentti](dokumentaatio/vaatimusmaarittely.md)

- [Testausdokumentti](dokumentaatio/testausdokumentti.md)

- [Työaikakirjanpito](dokumentaatio/Tyoaikakirjanpito.md)

- [Changelog](dokumentaatio/changelog.md)

- [Arkkitehtuuri](dokumentaatio/arkkitehtuuri.md)

- [Releases](https://github.com/JoonaPietarinen/ot-harjoitustyo/releases)

## Käynnistys

Peli toimii sekä Linuxilla että Windowsilla.

Asenna riippuvuudet:

```bash
poetry install
```

Käynnistä peli:

Pygame:

```bash
poetry run invoke start
```

Konsoli:

```bash
poetry run invoke start-console
```

Peli avautuu pygame-ikkunassa.

### Pelin ohjaus

- `w` = ylös
- `a` = vasen
- `s` = alas
- `d` = oikea
- `u` = käytä juoma
- `q` = lopeta peli


## Testaus

Testit voi suorittaa komennolla:

```bash
poetry run invoke test
```

### Testikattavuus

Testikattavuusraportin voi generoida komennolla:

```bash
poetry run invoke coverage-report
```

Generoidun raportin voit löytää _htmlcov_-hakemistosta.

### Pylint

Pylint tarkistuksen voi suorittaa komennolla:

```bash
poetry run invoke lint
```
