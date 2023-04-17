# Status

Fast and friendly SP admin client. spadmin.py is getting better and better day after day and we are happy to share our results with you.

Global spadmin.py development progress status: 

![spadmin progress](https://progress-bar.dev/50/)

# aktuális toDo-k

## beszíneztem a mount és drive parancsokat
- ehhez rendbe kell majd tenni az umount részt. Elnézést. 

Színezendő üzenetek:

## q proc
- ANR8805I Labeling volumes in library DELLML3; 5 volume(s) labeled.
- ANR8805I Labeling volumes in library DELLML3; 20 volume(s) labeled.\

- Keresni kell a többit!

## consolemode
- külön ablak:
   - macOS -> open -a iTerm ./spadmin.py
   - WSL 

## library manager opció bevezetése
- @Marcell:, ha van ilyen akkor a sh drive-nak ott kell futnia és azt ki kellene szoláglnia pexpect-nek
- sh drive: érdemes lenne az összes funkciót átvinni a régiből (sessiosn, process adatok)

## rl sql max row
- fetch first 100 rows only bevezetése és opciók + .ini
- cache_prefetch megírása
- rlwordseparation van ez még? meg lehetne tartani

## @_flex
- WSL doksi és dsmadmc-s teszt Microsoft Windows-on
- Ha az opciók végén = jel van, akkor az még az előzőhöz tartozik! ...
- kisbetű nagybetű alias, grep (az alias-oknál kikapcsoltam)
- alias regexp generator: SESs+, DISKs+
- header színes vágó megoldás (ez átkerült a data kiíróba is, ha az utolsó előtti oszlop nem férne ki) tesztelni kell, hoyg stabil-e

## inifile / program paraméterek
- össze kell őket fésülni

## induláskor prereq check
- os, python
- modulok
- fájlok


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
- > filename vagy outfile <filename>

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