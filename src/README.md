# spadmin.py


### prerequisites

- macOS, Linux, Linux konténer, Micrsoft Windows WSL
- python3
- python modulok (prereq.sh)
	- pip install termcolor readline pexpect readchar
    - Marcell - új mac-jén teszt: 
      - pip3 install pexpect 
      - pip3 install termcolor 
      - pip3 install readchar
      - pip3 install gnureadline
- dsmamdc v8.1.20
- dsmserv v8.1.20

## dsmadmc kezelés pexpect modullal 

## readline

Még nem tiszta 100%-ban, hogy mi a különbség a readline és a gnureadline között, de valami különbség biztosan van. Marcellnél GNU van, nálam sztem nem az. A Linux-okon valószínűleg GNU.

## Működő funkciók

./spadmin paraméterek

```
$ ./spadmin.py --help
usage: spadmin.py [-h] [-a AUTOEXEC] [-b BASECOMMANDNAME] [-c] [-d] [-f] [-i INIFILENAME] [-l LOGFILENAME] [-m] [-n] [-p] [-s] [-se SERVERADDRESS]
                               [-t TEXTCOLOR] [-u] [-v] [-w]

Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager.

options:
  -h, --help            show this help message and exit
  -a AUTOEXEC, --autoexec AUTOEXEC
                        autoexec command(s). Enclose the commands in quotation marks " " when multiple commands are separated by: ;
  -b BASECOMMANDNAME, --basecommandname BASECOMMANDNAME
                        custom base command name, default: SHow
  -c, --consoleonly     run console only mode!
  -d, --debug           debug messages into log file
  -f, --fetch           enable SQL prefetch queries
  -i INIFILENAME, --inifilename INIFILENAME
                        ini filename
  -l LOGFILENAME, --logfilename LOGFILENAME
                        log filename
  -m, --norlsqlcache    no cache for SQL queries in reradline
  -n, --norlsqlhelper   no SQL queries in reradline
  -p, --prereqcheck     prerequisite check
  -s, --disablerl       disable readline functionality
  -se SERVERADDRESS, --SErveraddress SERVERADDRESS
                        spadmin uses the server stanza to determine the server to connects to
  -t TEXTCOLOR, --textcolor TEXTCOLOR
                        specify the text color [default: "white"]
  -u, --nohumanreadable
                        no human readable conversions
  -v, --version         show version information
  -w, --nowelcome       no welcome messages

Thank you very much for downloading and starting to use it!
```

```
./spadmin.py -a "SHow Stgp; quit"

 ███████╗ ██████╗   █████╗  ██████╗  ███╗   ███╗ ██╗ ███╗   ██╗     ██████╗  ██╗   ██╗
 ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██║ ████╗  ██║     ██╔══██╗ ╚██╗ ██╔╝
 ███████╗ ██████╔╝ ███████║ ██║  ██║ ██╔████╔██║ ██║ ██╔██╗ ██║     ██████╔╝  ╚████╔╝
 ╚════██║ ██╔═══╝  ██╔══██║ ██║  ██║ ██║╚██╔╝██║ ██║ ██║╚██╗██║     ██╔═══╝    ╚██╔╝
 ███████║ ██║      ██║  ██║ ██████╔╝ ██║ ╚═╝ ██║ ██║ ██║ ╚████║ ██╗ ██║         ██║
 ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝         ╚═╝

           *             ,
                       _/^\_
                      <     >
     *                 /.-.\         *
              *        `/&\`                   *
                      ,@.*;@,
                     /_o.I %_\    *
        *           (`'--:o(_@;
 *                  /`;--.,__ `')             *
                  ;@`o % O,*`'`&\   *
            *    (`'--)_@ ;o %'()\      *
                 /`;--._`''--._O'@;
                /&*,()~o`;-.,_ `""`)
     *          /`,@ ;+& () o*`;-';\ *
               (`""--.,_0 +% @' &()\          *
               /-.,_    ``''--....-'`)  *
          *    /@%;o`:;'--,.__   __.'\            *
              ;*,&(); @ % &^;~`"`o;@();         *
              /(); o^~; & ().o@*&`;&%O\    *
        jgs   `"="==""==,,,.,="=="==="`
           __.----.(\-''#####---...___...-----._
         '`         \)_`"""""`

 Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager

= Welcome! Enter any IBM Spectrum Protect commands and if you're lost type Help!
= We're trying to breathe new life into this old school character based management interface.
= Once you start to use it, you can't live without it!!! 😀
= Python3 [3.11.6 (main, Nov  2 2023, 04:51:19) [Clang 14.0.0 (clang-1400.0.29.202)]]
= Your current Operating System platform is: macOS-12.7.1-x86_64-i386-64bit
= Terminal properties: [168x47]
= Current version: v1.4.1

 Short HELP:

    Use: "QUIt", "BYe", "LOGOut" or "Exit" commands to leave the program or
    Use: "SPadmin SHow LOG" or "SPadmin SHow LOCALLOG" to load the log file!

    Tip of the day: Use grep and regexp together, eg.: show actlog | grep ANR....E

 Your license is valid until 2099-01-01!

Loading rules: [100.0%=================================================================================================================================================]
SQL prefetch for faster readline queries...
----------- ----------- ----- ------ ------- ------- - ---- ---- ---- ----
PoolName    DeviceClass Coll  EstCap PctUtil PctMigr C High LowM Recl Next
----------- ----------- ----- ------ ------- ------- - ---- ---- ---- ----
ARCHIVEPOOL DISK                 0 B     0.0     0.0 N  90   70
BACKUPPOOL  DISK                 0 B     0.0     0.0 N  90   70       FILE
FILE        DC_FILE     GROUP  8 GiB     2.2     2.2    90   70   60
SPACEMGPOOL DISK                 0 B     0.0     0.0 N  90   70
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Program execution time: 6 s
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Background dsmadmc processes cleaning...
```

## rules fájl használata

### 1-es szint:

Ez a legegyszerűbb, mert egyelőre ezeket a parancsrészleteket külön kezeljük. A leírásuk így nézni ki:

```
$->ACCept
```

### 2-es szint:

A 2-es szintet és a többi ezt követő szintet egyelőre közös helyen kezeljük. A leírása így néz ki:

```
ACCept -> Date
```

### 3-as szint (innen jönnek az IBM SP opciók, mint lehetséges parancselemek):

Ha csak sima három szóból álló parancsról van szó, akkor a következő:

```
SPadmin SHow -> CONFig
```

Ha csak sima három szóból álló parancsról van szó és valami szabadszöveges segítséget akarunk adni, akkor valami ilyet lehet:

```
DEFine DEVclass -> <GIVE_a_valid_device_class_name>
```

Ha csak egy opció van ezen a szinten és szabad az értéke:

```
BAckup DB              -> PASSword=
```

Ha opciók is tartoznak hozzá:

```
BAckup DB              -> Type=
BAckup DB Type=        -> Type=Incremental
BAckup DB Type=        -> Type=Full
BAckup DB Type=        -> Type=DBSnapshot
```

Ha tartozik hozzá SQL lekérdezés:

```
ASsign DEFMGmtclass    -> select domain_name from domains
ACTivate POlicyset     -> select domain_name from domains
```

Ha tartozik hozzá SQL lekérdezés és az SQL lekérdezésben fel akarunk használni egy a parancssorban korábban megadott szót:

```
DEFine ASSOCiation \w+     -> select schedule_name from client_schedules where domain_name like upper( '-2' )
```

Ha opció és tartozik hozzá SQL lekérdezés:

```
BAckup DB              -> DEVclass=
BAckup DB DEVclass=    -> select concat( '%PREFIX%', devclass_name ) from devclasses {Prefix: -1}
```

### 4-es szint

Ha tartozik hozzá SQL lekérdezés és az SQL lekérdezésben fel akarunk használni egy a parancssorban korábban megadott szót:

```
DEFine ASSOCiation \w+ \w+ -> select node_name from nodes where domain_name like upper( '-3' )
```

## A következő parancsok mennek:

ACCept
- Date
	
ACTivate
- POlicyset  

ASsign
- DEFMGmtclass    

BAckup
- DB
- DEVCONFig
- VOLHistory
	
DEFine
- ASSOCiation

DELete
- STGpool

REMove 
- Node
 
SHow
- STGpools

Reload - újraolvassa a rule fájt

SPadmin

- SET DEBUG - bekpcsolja a debog szintű log-olást
- SHow
	- ALIases - kiírja az alias-okat    
	- CAche - kiírja a cache statisztikát   
	- CONFig    
	- ENVinronment    
	- EXtras - kiírja a parancs után megadott extra pipe opciókat [DEV]    
	- Log - megnyitja az spadmin log-ját   
	- PROCessinfo    
	- RULes - kiírja a szabályokat, amit a readline használ   
	- VERsion - kiírja az spadin verzióját
		  
- UNSET DEBUG - kikapcsolja a debug szintű log-olást

- UPDate ???   

- VERsion !!!ez nem kell!!!

##
