# toDos

## readline vs. GNUreadline vs. ...
- Microsoft Windows WSL
- esetleg CygWin

## getopt, GNU getopt, parameters
- Kell valami paraméterkezelés: --debug 1 --commands q sess; q log; quit --version --help --prereqcheck 
 
## Level 1 
- no recursion! Test Ezt m;g ;rdemes lenne megnézni
- case problem lower: QUIt       Query

## TESTs
- on Linux
- on MS Windows 10, 11
	- cygwin
	- WSL
	- Microsoft Windows 7 + python 3.8 nem megy, mert nincs readline és a színezés sem ment
	- latest Microsoft Windows 10 + python 3.10.6 ugyan az: nics readline és szín
	- prompt_toolkit megy Microsoft Windows-on
	
## Plugin handler
- 

## ADD: popen?, pexpect?

## Table printer
- text (colored, left, right, center, cut, ?)
- PDF
- CSV
- > filename

Hogyan kellene kinéznie:

=================== ========================================================================================================================
Date                Actlog
=================== ========================================================================================================================
08/16/2022 09:40:02 ANR8592I Session 136369 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                    certificate TSM Self-Signed Certificate.  (SESSION: 136369)
08/16/2022 09:40:02 ANR8592I Session 136369 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                    certificate TSM Self-Signed Certificate.  (SESSION: 136369)

=================== ========================================================================================================================
 Date                Actlog
=================== ========================================================================================================================
08/16/2022 09:40:02 ANR8592I Session 136369 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                    certificate TSM Self-Signed Certificate.  (SESSION: 136369)
08/16/2022 09:40:02 ANR8592I Session 136369 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                    certificate TSM Self-Signed Certificate.  (SESSION: 136369)

=================== ========================================================================================================================
| Date            | | Actlog                                                                                                               |
=================== ========================================================================================================================
08/16/2022 09:40:02 ANR8592I Session 136369 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                    certificate TSM Self-Signed Certificate.  (SESSION: 136369)
08/16/2022 09:40:02 ANR8592I Session 136369 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                    certificate TSM Self-Signed Certificate.  (SESSION: 136369)

** Fontos anna a kezelése, hogy mi van akkor, ha nem fér ki a tábla **

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
- log
- actlog
	
# Rules file regexp consolidation
OK? - regexp pattern generator okés (még az opciók kezelése visszavan)

# test driven / cases
- github actions
- ? kellene már valami tesztelő megoldás, akár a függvények hivogatásával

# command executor
OK - handle it with the readline completer! Igen 
OK - q sess; q dom; show time
- alias commands

# Code brush
- regexp logging
- import kupac
- 

# 1 Bináris mind felett
- ? Microsoft Windows, macOS, Linux