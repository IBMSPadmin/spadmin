# spadmin.py

Maradhat ez a név. Amivel megvagyunk:

### prerequisites

- macOS, Linux, Linux konténer, Microst Windows WSL
- python3
- pyton modulok
	- pip install pexpect termcolor readline click toolz wcwidth
- dsmamdc v8.1.15

## dsmadmc kezelés pexpect modullal

## readline

Még nem tiszta 100%-ban, hogy mi a különbség a readline és a gnureadline között, de valami van. Marcellnél GNU van, nálam sztem nem az. A Linux-okon valószínűleg GNU.

## Működő funkciók

./spadmin paraméterek

```
$ ./spadmin.py -h
usage: spadmin.py [-h] [--consoleonly] [-c [COMMANDS]] [-d] [-i [INIFILENAME]] [-l [LOGFILENAME]] [-m] [-n] [-p] [-r] [-v]

Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager.

options:
  -h, --help            show this help message and exit
  --consoleonly         run console only mode!
  -c [COMMANDS], --commands [COMMANDS]
						autoexec command(s). Enclose the commands in quotation marks " " when multiple commands are separated by: ;
  -d, --debug           debug messages into log file
  -i [INIFILENAME], --inifilename [INIFILENAME]
						ini filename
  -l [LOGFILENAME], --logfilename [LOGFILENAME]
						log filename
  -m, --norlsqlcache    no cache for sql queries in reradline
  -n, --norlsqlhelpepr  no sql queries in reradline
  -p, --prereqcheck     prerequisite check
  -r, --disablerl       disable readline functionality
  -v, --version         show version information

Thank you very much for downloading and starting to use it!
```

```
$ ./spadmin.py -c 'SHow Stgp; quit'

 ███████╗ ██████╗   █████╗  ██████╗  ███╗   ███╗ ██╗ ███╗   ██╗     ██████╗  ██╗   ██╗
 ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██║ ████╗  ██║     ██╔══██╗ ╚██╗ ██╔╝
 ███████╗ ██████╔╝ ███████║ ██║  ██║ ██╔████╔██║ ██║ ██╔██╗ ██║     ██████╔╝  ╚████╔╝
 ╚════██║ ██╔═══╝  ██╔══██║ ██║  ██║ ██║╚██╔╝██║ ██║ ██║╚██╗██║     ██╔═══╝    ╚██╔╝
 ███████║ ██║      ██║  ██║ ██████╔╝ ██║ ╚═╝ ██║ ██║ ██║ ╚████║ ██╗ ██║         ██║
 ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝         ╚═╝

 Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager

= Welcome! Enter any IBM Spectrum Protect commands and if you're lost type Help!
= We're trying to breathe new life into this old school character based management interface.
= Once you start to use it, you can't live without it!!! 😀
= Python3 [3.10.6 (main, Aug 30 2022, 05:12:36) [Clang 13.1.6 (clang-1316.0.21.2.5)]]
= Your current Operating System platform is: macOS-12.5.1-x86_64-i386-64bit
= Terminal properties: [155x45]

Loading rules: [100.0%====================================================================================================================================]

 Short HELP:

	  Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program or
	  use: "REload" to reload the rule file! and
	  use: "SHow LOG" to reach the local log file!

-------------- ----------------- ----- -------------- ------------- ---------- --------- -------- ------ --------------
Pool Name      Device class      Coll. Est. Cap. (GB) Pct. Utilized Pct. Migr. High Mig. Low Mig. Recl.  Next
-------------- ----------------- ----- -------------- ------------- ---------- --------- -------- ------ --------------
CEVA_CT        DC_TS3200_LTO4_02 NO           12668.0          26.8                                  100
CEVA_NAS_BD    DISK                             200.0           8.1        8.1        80       60        CEVA_NAS_BT
CEVA_NAS_BT    DC_TS3200_LTO4_05 GROUP        32005.9          42.2       17.2       100       99     60
CEVA_WINDIR_BD DISK                              10.0           6.9        0.0        90       70        CEVA_WIN_BT
CEVA_WIN_BD    DISK                             400.0           0.0        0.0        90       10        CEVA_WIN_BT
CEVA_WIN_BT    DC_TS3200_LTO4_01 NO           11829.3          28.7       33.3       100       99     60
CLOUDPOOL                                           0
EG_LINUX_BD    DISK                             100.0           0.0        0.0        90       70        EG_LINUX_BT
EG_LINUX_BT    DC_TS3200_LTO4_04 NO            8940.7           0.3        1.0       100       99     60
EG_MAC_BD      DISK                             200.0           0.0        0.0        90       70        EG_LINUX_BT
EG_MAC_BT      DC_TS3200_LTO4_03 NO               0.0           0.0        0.0         0        0     60 EG_LINUX_BT
SPACEMGPOOL    DISK                               0.0           0.0        0.0        90       70
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Program execution time: 0:00:03.986163
-----------------------------------------------------------------------------------------------------------------------------------------------------------
Background dsmadmc processes cleaning...

19:02:49 Fri Sep 09 [flex@MBP16:[~/gith/spadmin/completer-poc] [0]
$
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
		  
- UNSET DEBUG - kikpcsolja a debog szintű log-olást

- UPDate ???   

- VERsion !!!ez nem kell+

##