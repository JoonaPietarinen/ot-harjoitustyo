# Ohjelmistotekniikka, harjoitustyö

Olen toteuttamassa yksinkertaista _**roguelike-tyyppistä luolastoseikkailupeliä**_, jossa pelaaja etenee _vihollisia_ ja _ansoja_ sisältävissä tasoissa, kerää **esineitä** ja pyrkii selviytymään mahdollisimman pitkälle. 

## Dokumentaatio

- [Määrittelydokumentti](dokumentaatio/vaatimusmaarittely.md)

- [Työaikakirjanpito](dokumentaatio/Tyoaikakirjanpito.md)

- [Changelog](dokumentaatio/changelog.md)

## Käynnistys

Peli toimii sekä Linuxilla että Windowsilla.

Asenna riippuvuudet:

```bash
poetry install
```

Käynnistä peli:

```bash
poetry run invoke start
```

### Pelin ohjaus

- `w` = ylös
- `a` = vasen
- `s` = alas
- `d` = oikea
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
