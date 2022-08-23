# toDos

## Fontos!

- pexpect tudjon két dsmamdc-t indítani
- pexpect tudjon másik szerverhez csatlakozni
- pexpect timout lekezelése, mert még mindig előjön

```
[CLOUDTSM1] > q STG
Traceback (most recent call last):
  File "/Users/flex/GitHub/spadmin/completer-poc/./spadmin.py", line 734, in <module>
	for textline in DSM2.send_command2( DSM2, line ):
  File "/Users/flex/GitHub/spadmin/completer-poc/./spadmin.py", line 409, in send_command2
	tsm.expect( [ self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF ] )
  File "/usr/local/lib/python3.10/site-packages/pexpect/spawnbase.py", line 343, in expect
	return self.expect_list(compiled_pattern_list,
  File "/usr/local/lib/python3.10/site-packages/pexpect/spawnbase.py", line 372, in expect_list
	return exp.expect_loop(timeout)
  File "/usr/local/lib/python3.10/site-packages/pexpect/expect.py", line 181, in expect_loop
	return self.timeout(e)
  File "/usr/local/lib/python3.10/site-packages/pexpect/expect.py", line 144, in timeout
	raise exc
pexpect.exceptions.TIMEOUT: Timeout exceeded.
<pexpect.pty_spawn.spawn object at 0x1083b39d0>
command: /usr/local/bin/dsmadmc
args: [b'/usr/local/bin/dsmadmc', b'-id=support', b'-pa=asdpoi123']
buffer (last 100 chars): 'q STG\r\n\r'
before (last 100 chars): 'q STG\r\n\r'
after: <class 'pexpect.exceptions.TIMEOUT'>
match: None
match_index: None
exitstatus: None
flag_eof: False
pid: 94120
child_fd: 7
closed: False
timeout: 30
delimiter: <class 'pexpect.exceptions.EOF'>
logfile: None
logfile_read: None
logfile_send: None
maxread: 2000
ignorecase: False
searchwindowsize: None
delaybeforesend: 0.05
delayafterclose: 0.1
delayafterterminate: 0.1
searcher: searcher_re:
	0: re.compile('Protect: .*')
	1: re.compile('tsm: .*')
	2: re.compile("more...   \\(\\<ENTER\\> to continue, 'C' to cancel\\)")
	3: re.compile("The character '#' stands for any decimal integer.")
	4: re.compile('Do you wish to proceed\\? \\(Yes \\(Y\\)/No \\(N\\)\\)')
	5: EOF

21:14:39 Mon Aug 22 [flex@MBP16:[~/gith/spadmin/completer-poc] [1]
```

- pexpect eldobja a fonalat a: help q node, help q lic, ... parancsokra

```
Traceback (most recent call last):
  File "/Users/flex/GitHub/spadmin/completer-poc/./spadmin.py", line 734, in <module>
	for textline in DSM2.send_command2( DSM2, line ):
  File "/Users/flex/GitHub/spadmin/completer-poc/./spadmin.py", line 409, in send_command2
	tsm.expect( [ self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF ] )
  File "/usr/local/lib/python3.10/site-packages/pexpect/spawnbase.py", line 343, in expect
	return self.expect_list(compiled_pattern_list,
  File "/usr/local/lib/python3.10/site-packages/pexpect/spawnbase.py", line 372, in expect_list
	return exp.expect_loop(timeout)
  File "/usr/local/lib/python3.10/site-packages/pexpect/expect.py", line 169, in expect_loop
	incoming = spawn.read_nonblocking(spawn.maxread, timeout)
  File "/usr/local/lib/python3.10/site-packages/pexpect/pty_spawn.py", line 467, in read_nonblocking
	incoming += super(spawn, self).read_nonblocking(size - len(incoming))
  File "/usr/local/lib/python3.10/site-packages/pexpect/spawnbase.py", line 181, in read_nonblocking
	s = self._decoder.decode(s, final=False)
  File "/usr/local/Cellar/python@3.10/3.10.6_1/Frameworks/Python.framework/Versions/3.10/lib/python3.10/codecs.py", line 322, in decode
	(result, consumed) = self._buffer_decode(data, self.errors, final)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xae in position 65: invalid start byte
```

- WSL doksi és dsmadmc-s teszt Microsoft Windows-on
- python 3.6.8 RH Linux ✅, python 3.10.6 macOS ✅
- python 2.7.5 kompatibilitást ❌ meg kellene csinálni! Nekem eddig sikerült:

- rules fájlban listakezelés
- opciókra ( ...=... ) egy stabil megoldás
- és ez az egészet úgy, hogy tovább kezelődjön
- spsqlengine több paraméter kezelésére felkészíteni vagy lebutítani sima lekérdezésekre és akkor a végén lévő kreső keres mindig mintákat
- ha mindenhol ez a kereső kell, akkor legyen melőle sub()

```
Traceback (most recent call last):
  File "./spadmin", line 647, in <module>
	rlprompt       = '[' + colored( DSM.send_command_array( DSM, 'select SERVER_NAME from STATUS' )[ 0 ], 'white', attrs=[ 'bold' ] ) + '] ' + colored( '>', 'red', attrs=[ 'bold' ] ) + ' '
TypeError: unbound method send_command_array() must be called with DSM instance as first argument (got classobj instance instead)
```

## Directory struct?

./
 spadmin.py
 spadmin.rules
 spadmin.log

	/cache
	/reports
	/history
	/timemachine

## readline vs. GNUreadline vs. ...
- Microsoft Windows WSL
- esetleg CygWin

## getopt, GNU getopt, parameters
- Kell valami paraméterkezelés: --debug 1 --commands 'q sess; q log; quit' --version --help --prereqcheck --consoleonly
 
## Level 1 
- no recursion! Teszt Ezt még érdemes lenne megnézni!!!
- case problem lower: QUIt       Query és Q STG!!!

## TESTs
- on Linux RH ✅
- on MS Windows 10, 11
	- cygwin
	- WSL ✅
	- Microsoft Windows 7 + python 3.8 nem megy, mert nincs readline és a színezés sem ment ❌
	- latest Microsoft Windows 10 + python 3.10.6 ugyanaz: nincs readline és szín ❌
	- prompt_toolkit megy Microsoft Windows-on ❓
	
## Plugin handler
- 

## ADD: popen?, pexpect?
- egyelőre pexpect

## Table printer
- text (colored, left, right, center, cut, ?)
- PDF
	- TSM riport q node, q sched, q vol acc reado, unava, q lic
- HTML email?
- CSV
- > filename

PROC, ACTLOG: Hogyan kellene kinéznie:

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

** Fontos annak a lekezelése, hogy mi van akkor, ha nem fér ki a tábla **

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
