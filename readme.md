# dyfi.py

Yksinkertainen cronjobina ajettava dy.fi domain päivitin

## Nimen lisääminen

    $ dyfi.py --add

ja syötä käyttäjä, salasana ja dy.fi nimi kysyttäessä.

## Muokkaus

    $ dyfi.py --edit

dyfi.py avaa oletus editorin (ympäristömuuttuja $EDITOR) tai 'nano' jos $EDITOR
muuttujaa ei ole asetettu

## Käyttö

dyfi.py on suunniteltu ajettavaksi cronjobina, esim. kerran päivässä. dyfi.py
pitää kirjaa mikä on viimeisin IP osoite sekä milloin nimi on viimeksi 
päivitetty, eikä yritä edes päivittää IP osoitetta jos edellisestä 
päivityksestä on alle 5 päivää tai koneen IP-osoite ei ole vaihtunut.

cronjob lisätään ajamalla

    $ cronjob -e

ja lisäämällä rivit

    @reboot dyfi.py -u
    37 16 * * * dyfi.py -u

ensimmäinen rivi tarkoittaa, että dyfi päivitys ajetaan joka kerta kun kone
käynnistyy, ja toinen rivi sitä että dyfi.py tarkistaa päivityksen tarpeen
kerran päivässä kun kellon on 16:37. On suositeltavaa, että minuuttiosuus
asetetaan joksikin satunnaisluvuksi 0 ja 59 välillä, jotta dy.fi palvelimet
eivät kuormitu, koska kaikki haluavat päivittää dy.fi nimensä samaan aikaan.
