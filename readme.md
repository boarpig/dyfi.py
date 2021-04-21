# dyfi.py

Yksinkertainen cronjobina ajettava dy.fi domain päivitin. dyfi.py vaatii
toimiakseen python3 ja [Requests](http://docs.python-requests.org/en/latest/)
kirjaston

## Asennus

Kloonaa dyfi.py sopivaan kansioon

```
    $ git clone https://github.com/boarpig/dyfi.py ~/dyfi.py
    $ sudo cp ~/dyfi.py /usr/bin/dyfi.py
    $ sudo chmod 0755 /usr/bin/dyfi.py

## Käyttö lyhyesti

    # dyfi.py --add
    Käyttäjä: kalle.kayttaja@esimerkk.fi
    salasana: salasana123
    Domain nimi: host.dy.fi
    # dyfi.py -u

## Nimen lisääminen

    # dyfi.py --add

ja syötä käyttäjä, salasana ja dy.fi nimi kysyttäessä.

## Muokkaus

    # dyfi.py --edit

dyfi.py avaa oletus editorin (ympäristömuuttuja $EDITOR) tai 'nano' jos $EDITOR
muuttujaa ei ole asetettu

## Käyttö

dyfi.py:n mukana tulee systemd service ja timer unit-tiedostot. 

### timerin ajaminen roottina

Aseta systemd/ hakemistosta löytyvät `dyfi.service` ja `dyfi.timer` tiedostot
`/etc/systemd/system/` hakemistoon ja aktivoi ja käynnistä timer.

```
# cp systemd/dyfi.{service,timer} /etc/systemd/system
# systemctl start dyfi.timer
```

**HUOM!** Tämä olettaa, että `dyfi.py` on asennettu `/usr/bin/` hakemistoon. Jos
`dyfi.py` on jossain muualla, muokkaa `dyfi.service` tiedoston `ExecStart=`
osiota.

### timerin ajaminen tavallisena käyttäjänä

Aseta systemd/ hakemistosta löytyvät `dyfi.service` ja `dyfi.timer` tiedostot
`~/.config/systemd/user/` hakemistoon ja aktivoi ja käynnistä timer.

```
$ cp systemd/dyfi.{service,timer} ~/.config/systemd/user/
$ systemctl --user start dyfi.timer
```

**HUOM!** Tämä olettaa, että `dyfi.py` on asennettu `/usr/bin/` hakemistoon. Jos
`dyfi.py` on jossain muualla, muokkaa `dyfi.service` tiedoston `ExecStart=`
osiota.

### dyfi.py:n ajaminen cronilla

cronjob lisätään ajamalla

    # crontab -e

ja lisäämällä rivit

    @reboot /usr/bin/dyfi.py -u
    0 */4 * * * /usr/bin/dyfi.py -u

Huomaa, että on suositeltavaa laittaa absoluuttinen polku dyfi.py ohjelmaan tai
cron ei muuten välttämättä löydä sitä.

Rivit tarkoittavat sitä, että dyfi päivitys tarkistetaan joka kerta kun kone
käynnistyy, sekä neljän tunnin välein. Voit syöttää minuutti kohtaan minkä 
vain kellonajan, mutta on suositeltavaa, että minuuttiosuus asetetaan 
joksikin satunnaisluvuksi 0 ja 59 välillä, jotta dy.fi palvelimet eivät 
kuormitu, jos vaikka kaikki haluavat päivittää dy.fi nimensä samaan aikaan
tasatuntina. 

On turvallista ajaa päivitysohjelma vaikka kerran tunnissa, sillä se ei ota
yhteyttä dy.fi palvelimiin, kuin sillon, jos se kokee päivityksen
tarpeelliseksi.

Lisätietoja cronjobien tekemiseen löytyy [crontabin man-sivulta](http://manpages.debian.net/cgi-bin/man.cgi?query=crontab&sektion=5)
tai komentorivillä

    $ man 5 crontab
