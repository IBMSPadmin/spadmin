# Status

Global spadmin.py development progress status: 

![spadmin progress](https://progress-bar.dev/40/)

# aktuális toDo-k

@_flex
- WSL doksi és dsmadmc-s teszt Microsoft Windows-on
- alias kezelő parancsok
- "intelligens" rule dictionary betöltő function és akkor nem kell az a sok kavarás az owncommand-ban

@Marcell
- színezés
~~- columnar: üres sorok (valahogy megint viszakrült az üres sor a végére) és sor végi space-ek eltűntetése~~
- columnar: az utolsó oszlop több karaktert használ, mint illene. Ezeket eliminálni kellene
- columnar: kezelni kell, ha üres adat megy át. Akkor csak a fejléc legyen kiírva
~~- alias kezelés valahogy az inifájlba~~
~~- more / grep: (a példaparancs rá: **SPadmin SHow EXtras | grep | invgrep | count**)~~ 

## Fontos!

- pexpect tudjon másik szerverhez csatlakozni

- rules fájlban listakezelés???
- opciókra ( ...=... ) egy stabil megoldás
- és ez az egészet úgy, hogy tovább kezelődjön
- spsqlengine több paraméter kezelésére felkészíteni vagy lebutítani sima lekérdezésekre és akkor a végén lévő kereső keres mindig mintákat (ez a cache miatt lenne jó)
- ha mindenhol ez a kereső kell, akkor legyen belőle sub()


## Directory struct?

./
 spadmin.py
 spadmin.rules
 spadmin.log

	/cache
	/reports
	/history
	/timemachine
	/logs

## readline vs. GNUreadline vs. ...
- Microsoft Windows WSL
- esetleg CygWin
 
## kell valami setup wizard is az elejére 
 
## Level 1 
- case problem lower: QUIt       Query és Q STG!!!

## TESTs
- on Linux RH ✅
- on MS Windows 10, 11
	- cygwin ?
	- WSL ✅
	- Microsoft Windows 7 + python 3.8 nem megy, mert nincs readline és a színezés sem ment ❌
	- latest Microsoft Windows 10 + python 3.10.6 ugyanaz: nincs readline és szín ❌
	- prompt_toolkit megy Microsoft Windows-on ❓
	
## Plugin handler
- ?

## Table printer
- text (colored, left, right, center, cut, ?)
- PDF
	- TSM riport q node, q sched, q vol acc reado, unava, q lic
- HTML email?
- CSV
- > filename

Színezés szekvenciája:

!!! még a színezések előtt meg kell tudni a méretét, hogy lássuk melyik a leghosszabb sor, mert a fejléc arra fog elkészülni és a többi sor is azzal lesz finomhangolva !!! 
- Ha van grep akkor azt ki kellene emelni (Mi van ha pont ott törik meg???)
- Ugyenez igaz ha valami mintát emelünk ki. A grep kiemelése nem annyira fontos, de a minta kiemelés az nem maradha ki.
- Ha a mintára megcsináljuk, akkor maradhat a grep-nél is: tehát meg kell csinálni
- Engedjük el a teljes sor kiszínezését, mert úgy könnyebb

{RED, ANR8592I} Session 136369 connection is using protocol TLSV12, cipher specification {RED, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384}, certificate TSM Self-Signed Certificate.  (SESSION: 136369)
Ha sortöréskor volt elkezdett szín, akkor azzal kell az újat is elkezdeni.

- Kell-e törni a sort, ha nem kész.
- Kell: van-e épp olyan szín, aminél törik a sor? Ha igen, akkor azzal kell majd kezdeni a következő sort!
- 

# Start console 

Azaz lehessen ablakban valami mást nyitni.

- log
- actlog
	
# test driven / cases
- github actions
- ? kellene már valami tesztelő megoldás, akár a függvények hivogatásával

# Code brush
- regexp logging
- import kupac

# 1 Bináris mind felett
- ? Microsoft Windows, macOS, Linux