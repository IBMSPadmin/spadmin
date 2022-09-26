# Status

Global spadmin.py development progress status: 

![spadmin progress](https://progress-bar.dev/40/)

# aktuális toDo-k

ANR8805I Labeling volumes in library DELLML3; 5 volume(s) labeled.
ANR8805I Labeling volumes in library DELLML3; 20 volume(s) labeled.\

Volume MKP048M8 (storage pool VMW_B_T), Target Pool VMW_B_T, Moved Files: 0, Moved Bytes: 0 bytes, Deduplicated Bytes: 0 bytes, Unreadable Files: 0, Unreadable Bytes: 0 bytes. Current Physical File (bytes): 128 MB Waiting for mount of output volume MKP058M8 (26 seconds).

Volume MKP048M8 (storage pool VMW_B_T), Target Pool VMW_B_T, Moved Files: 0, Moved Bytes: 0 bytes, Deduplicated Bytes: 0 bytes, Unreadable Files: 0, Unreadable Bytes: 0 bytes. Current Physical File (bytes): 128 MB Current output volume(s): MKP058M8.

Volume MKP056M8 (storage pool SQL_B_T), Target Pool SQL_B_T, Moved Files: 9, Moved Bytes: 90,012 MB, Deduplicated Bytes: 0 bytes, Unreadable Files: 0, Unreadable Bytes: 0 bytes. Current Physical File (bytes): 10,001 MB Current input volume: MKP056M8. Current output volume(s): MKP074M8.

TYPE=FULL in progress. Bytes backed up: 10 bytes. Current output volume(s): .
TYPE=FULL in progress. Bytes backed up: 1,978 MB. Current output volume(s): MKP060M8.

@_flex
- WSL doksi és dsmadmc-s teszt Microsoft Windows-on
~~- alias kezelő parancsok~~
~~- "intelligens" rule dictionary betöltő function és akkor nem kell az a sok kavarás az owncommand-ban~~
- Ha az opciók végén = jel van, akkor az még az előzőhöz tartozik!
~~- Kell egy másodperc humán kiíró m, H, d~~
- kisbetű nagybetű alias, grep (az alias-oknál kikapcsoltam)
- alias regexp generator: SESs+, DISKs+

-- -------- -------------------------
 # Commands
-- -------- -------------------------
 1    ~~alias~~
 2  console
 3    ~~debug~~
 4    ~~debug~~
 5   delete associations
 6     edit script
 7   fooooo
 8~~history~~
 9   ~~kill~~
10     load script
11    login
12   moveit
13  offline
14   online
15    reach
16   reload
17     save script
18      set server
19     show Expp
20     show LICences
21     show _backup
22     show activity
23     ~~show actlog~~
24     show adminevents
25     show archive_retention
26     show association
27     show avgTapeCap
28     show backup_retention
29     show backupperformance
30     show backuptotal
31     show clientarchiveperformance
32     show clientbackupperformance
33     show clientrestoreperformance
34     show clientretrieveperformance
35     show columns
36     show commands
37     show containerusage
38     show copydifference
39     show dbbackup
40     show dbsbackup
41     show dbspace
42     show deduppending
43     show defassociation
44     show devclass
45     show disks
46     show drives
47     show drvolume
48     show elog
49     show environment
50     show estgpools
51     show events
52     show expiration
53     show fillings
54     show inactive
55     show lasterror
56     show libvolumes
57     show maxscratch
58     show migrationperformance
59     show moveable
60     show movedataperformance
61     show nodebackup
62     show nodedelta
63     show nodeoccuopancy
64     show nodes
65     show paths
66     ~~show processes~~
67     show protectperformance
68     show reclaim
69     show reclamationperformance
70     show reorgopt
71     show replicationdifference
72     show replicationperformance
73     show ruler
74     show schedules
75     show scratches
76     show scripts
77     show servers
78     ~~show sessions~~
79     show status
80     ~~show stgpools~~
81     show summary
82     show timing
83     show transferrate
84     show veocc
85     show version
86     show vmallbackupstat
87     show vmbackupstat
88     show volreclaim
89     show volumestatus
90     show volumeusage
91    start dsmadmc
92 terminal

@Marcell
- színezés
~~- SPADMin show PROCessinfo~~
~~- columnar: üres sorok (valahogy megint viszakrült az üres sor a végére) és sor végi space-ek eltűntetése~~
~~- columnar: az utolsó oszlop több karaktert használ, mint illene. Ezeket eliminálni kellene~~
~~- columnar: kezelni kell, ha üres adat megy át. Akkor csak a fejléc legyen kiírva~~
~~- alias kezelés valahogy az inifájlba~~
~~- more / grep: (a példaparancs rá: **SPadmin SHow EXtras | grep | invgrep | count**)~~ 
~~- columnar: több helyen van fölösleges szóköz még mindig!~~
~~- more: nem működik, ha van sortörés~~
~~- orderby? sp stgp | orderby 3~~
~~- az alias-ok mindig felülíródnak az .ini-ben~~

## Fontos!

~~- pexpect tudjon másik szerverhez csatlakozni~~

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