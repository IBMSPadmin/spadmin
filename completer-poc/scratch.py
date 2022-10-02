# import queue
# import re
# import sys
# from typing import Sequence
# from typing.re import Match
#

from re import search, compile, findall

data = [ ["ANR8331I LTO volume SBO566L6 is mounted R/W in drive DRV1 (/dev/lin_tape/by-id/1068005803), status: DISMOUNTING."],
         ["ANR8330I LTO volume SBO376L6 is mounted R/W in drive DRV2 (/dev/lin_tape/by-id/1068006258), status: IN USE."],
        ["ANR8330I LTO volume SBO566L6 is mounted R/W in drive DRV1 (/dev/lin_tape/by-id/1068005803), status: IN USE."],
        ["ANR8330I LTO volume SBO376L6 is mounted R/W in drive DRV2 (/dev/lin_tape/by-id/1068006258), status: IN USE."],
        ["ANR8379I Mount point in device class DCLTO_02 is waiting for the volume mount to complete, status: WAITING FOR VOLUME."],
         ["ANR8329I LTO volume SBO376L6 is mounted R/W in drive DRV2 (/dev/lin_tape/by-id/1068006258), status: IDLE."]
       ]

for l in data:
    if search("ANR83(29|30|31|32|33)I.*", l[0]):
        print (l[0])
        for vol, rw_ro, drive, path, status in findall(compile(r'.* volume (.*) is mounted (.*) in drive (.*) \((.*)\), status: (.*)..*'), l[0]):
            print("Match: ", vol, rw_ro, drive, path, status)
    elif search("ANR8379I", l[0]):
        print(l[0])
        for devc, status in findall(compile(".* device class (.*) is waiting .*, status: (.*)..*"), l[0]):
            print("Match: ", devc, status)



quit(0)
# from colorama import Fore, Back, Style
# from termcolor import colored
# import humanbytes
#
# def yellow(match_obj):
#     for g in match_obj.groups():
#         if g is not None:
#             return Fore.YELLOW + match_obj.group() + Style.RESET_ALL
#
#
# text = "ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria."
# # print (text)
#
# text = text.replace("No match found using this criteria",
#                     ''.join([Fore.BLUE, "No match found using this criteria", Style.RESET_ALL]))
# # print (text)
#
# text = Fore.RED + text + Style.RESET_ALL
#
# # print (repr(text))
# # print (text)
# grep = "u"
#
# # RED
# #                                     Kek
# #    ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria RESET  . RESET
#
# text = re.sub(r"(" + grep + ")", yellow, str(text))
# # print (repr(text))
# # print (text)
#
# ansi_color_pattern = re.compile(r"\x1b\[.+?m")
#
# print("")
# print("")
# print("")
#
#
# def szinezo_jo(text: str, regexp: str, color: str):
#     match = re.search(regexp, text)
#     print(match)
#     if match:
#         before = text[0:match.start()]
#         # print(repr(before))
#         last_colors = re.findall("(\x1b\[.+?m)", before)
#         found_last_color = ''
#         if last_colors:
#             found_last_color = last_colors[-1]
#         return text.replace(match[0], colored(match[0], color) + found_last_color)
#     else:
#         return text
#
#
# # re.compile(r"(" + match.group() + ")").finditer(text):
#
# def szinezo(text: str, regexp: str, color: str):
#     ret = text
#     for m in reversed(list(re.finditer(regexp, text))):
#         last_colors = re.findall("(\x1b\[1m\x1b\[.+?m)", text[0:m.start()])
#         if last_colors:
#             ret = ''.join(
#                 [ret[0:m.start()], colored(ret[m.start():(m.start() + len(m.group()))], color, attrs=['bold']), last_colors[-1],
#                  ret[m.start() + len(m.group()):]])
#         else:
#             ret = text[0:m.start()] + colored(text[m.start():(m.start() + len(m.group()))], color, attrs=['bold']) + text[
#                                                                                                      m.start() + len(
#                                                                                                          m.group()):]
#     return ret
#
#
# text = "ANR2034E QUERY STGPOuOuLDuuuIRECTORY: No match found using this criteria."
# text = szinezo(text, "ANR....E.*$", "red")
# print(repr(text))
# text = szinezo(text, "TGPOuOuLDuuuIRECTORY", "blue")
# print(repr(text))
# text = szinezo(text, "u", "yellow")
# print(repr(text))
# text = szinezo(text, "O", "green")
# print(repr(text))
# text = szinezo(text, "i", "cyan")
# print(repr(text))
# print(text)
#
#
#
# def strip_color(cell_text):
#     matches = [match for match in ansi_color_pattern.finditer(cell_text)]
#     clean_text = cell_text
#     if matches:
#         clean_text = ansi_color_pattern.sub("", cell_text)
#     return clean_text, matches
#
#
# def colorize(text, code: Sequence[Match]):
#     ret = text
#     code_list = list(code)
#     marker = -1
#     for i, m in enumerate(code_list):
#         print("M: ", m, i)
#         if m.group() == Style.RESET_ALL:
#             marker -= 1
#             print("MarkerR: ", repr(code_list[marker].group()))
#             ret = "".join([ret[:m.start()+1], code_list[marker].group(), ret[m.start()+1:]])
#         else:
#             marker += 1
#             print("MarkerC: ", repr(code_list[marker].group()))
#             ret = "".join([ret[:m.start()], m.group(), ret[m.start():]])
#     return ret + Style.RESET_ALL
#
#
# # clean = "ANR2034E QUERY REPLICATION: No match found using this criteria."
# # text = "ANR2034E QUERY REPLICATION: No match found using this criteria."
# #
# # text = colored(text, "red")
# # value, code = strip_color(text)
# # print(colorize(value, code))
# #
# # text = text.replace("No match found using this c",
# #                     ''.join([Fore.BLUE, "No match found using this c", Style.RESET_ALL]))
# # value, code = strip_color(text)
# # print(colorize(value, code))
# #
# # text = text.replace("found",
# #                     ''.join([Fore.YELLOW, "found", Style.RESET_ALL]))
# # value, code = strip_color(text)
# # print(colorize(value, code))
# #
# # text = text.replace("i",
# #                     ''.join([Fore.CYAN, "i", Style.RESET_ALL]))
# # value, code = strip_color(text)
# # print(colorize(value, code))
#
#
# from wcwidth import wcwidth, wcswidth
#
#
#
# def get_visible_lenght(code, text):
#     s = ''
#     i = 0
#     while repr(s) != repr(text):
#         s = re.sub("(\x1b\[1m\x1b\[.+?m)",'',re.sub("(\x1b\[.+?m)",'',code[0:i]))
#         i += 1
#         print(repr(s))
#     return i-1
#
# def get_visible_lenght_vege(code, text):
#     s = ''
#     i = len(code)
#     while repr(s) != repr(text):
#         s = re.sub("(\x1b\[1m\x1b\[.+?m)",'',re.sub("(\x1b\[.+?m)",'',code[i:]))
#         i -= 1
#         print(repr(s))
#     return i+1
#
#
# def szinezd_ki(code, text):
#     if re.sub("(\x1b\[1m\x1b\[.+?m)",'',re.sub("(\x1b\[.+?m)",'',code)).startswith(str(text)):
#         return code[:get_visible_lenght(code, str(text))]
#     else:
#         return code[get_visible_lenght_vege(code, str(text)):]
#
# code = '\x1b[1m\x1b[31mANR2034E QUERY S\x1b[1m\x1b[34mTGP\x1b[1m\x1b[32mO\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[32mO\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34mLD\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34mIRECT\x1b[1m\x1b[32mO\x1b[0m\x1b[1m\x1b[34mRY\x1b[0m\x1b[1m\x1b[31m: No match fo\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[31mnd \x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[31ms\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31mng th\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31ms cr\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31mter\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31ma.\x1b[0m'
# text = 'ANR2034E QUERY STGPOuOuLDuuuIRECTORY: No match found u'
#
# print(text)
# print(code)
# # print("1", szinezd_ki(code,text))
#
# # text = 'sing this criteria.'
# # print("2", szinezd_ki(code,text))
# #
# # code = '\x1b[1m\x1b[31m 677 \x1b[0m'
# # text = 677
# #
# # print("3", szinezd_ki(code,str(text)))
#
# print (humanbytes.HumanBytes.format(float(128)*1024*1024, unit="BINARY_LABELS", precision=0))
# print (humanbytes.HumanBytes.format(float(128)*1024*1024, unit="METRIC_LABELS",precision=0))
# print (humanbytes.HumanBytes.format(int(31), unit="TIME_LABELS",precision=0))
# print (humanbytes.HumanBytes.format(int(65), unit="TIME_LABELS",precision=0))
# print (humanbytes.HumanBytes.format(int(128), unit="TIME_LABELS",precision=0))
# print (humanbytes.HumanBytes.format(int(3600*23), unit="TIME_LABELS",precision=0))

import columnar2
columnar = columnar2.Columnar()


stgp_data = [['DB2_DSK', 'DISK', '', '0 B', '0.0', '0.0', '80', '20', '', 'DB2_LTO'], ['DB2_LTO', 'DCLTO_01', 'GROUP', '18 TiB', '0.0', '40.0', '80', '70', '60', ''], ['FILES_CP', 'DCLTO_01C', 'NO', '3 TiB', '5.1', '', '', '', '100', ''], ['FILES_DSK', 'DISK', '', '2 TiB', '99.8', '1.2', '80', '20', '', 'FILES_LTO'], ['FILES_LTO', 'DCLTO_02', 'GROUP', '65 TiB', '14.7', '18.2', '80', '20', '60', ''], ['IBM_DEPLOY_CLIENT_POOL', 'IBM_DEPLOY_CLIENT_IMPORT', 'GROUP', '100 GiB', '10.0', '10.0', '90', '70', '60', ''], ['VMWARE_CTL', 'DISK', '', '50 GiB', '17.6', '17.6', '90', '70', '', ''], ['VMWARE_DSK', 'DISK', '', '10 TiB', '76.4', '0.0', '80', '20', '', 'VMWARE_LTO'], ['VMWARE_LTO', 'DCLTO_05', 'GROUP', '41 TiB', '33.4', '64.0', '80', '20', '60', '']]
actlog_data = [['09/26/2022 19:31:05', 'ANR8592I Session 846 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 846)'], ['09/26/2022 19:31:05', 'ANR0406I Session 846 started for node SP_VE_VMCLI (TDP VMware) (SSL tsm.in.useribm.hu[10.228.109.249]:37220). (SESSION: 846)'], ['09/26/2022 19:31:05', 'ANR0403I Session 846 ended for node SP_VE_VMCLI (TDP VMware). (SESSION: 846)'], ['09/26/2022 19:31:07', 'ANR8592I Session 847 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 847)'], ['09/26/2022 19:31:07', 'ANR0406I Session 847 started for node SP_VE_VMCLI (TDP VMware) (SSL tsm.in.useribm.hu[10.228.109.249]:37224). (SESSION: 847)'], ['09/26/2022 19:31:07', 'ANR0397I Session 847 for node SP_VE_VMCLI has begun a proxy session for node SP_VE_DATACENTER.  (SESSION: 847)'], ['09/26/2022 19:31:08', 'ANR0399I Session 847 for node SP_VE_VMCLI has ended a proxy session for node SP_VE_DATACENTER.  (SESSION: 847)'], ['09/26/2022 19:31:08', 'ANR0403I Session 847 ended for node SP_VE_VMCLI (TDP VMware). (SESSION: 847)'], ['09/26/2022 19:32:25', 'ANR8592I Session 849 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 849)'], ['09/26/2022 19:32:25', 'ANR0407I Session 849 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:54146). (SESSION: 849)'], ['09/26/2022 19:32:26', 'ANR0405I Session 849 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 849)'], ['09/26/2022 19:32:39', 'ANR0482W Session 841 for node IBM-OC-USERTSM.USR (DSMAPI) terminated - idle for more than 15 minutes. (SESSION: 841)'], ['09/26/2022 19:33:28', 'ANR0944E QUERY PROCESS: No active processes found. '], ['09/26/2022 19:33:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS ONLYWAITERS=YES '], ['09/26/2022 19:33:29', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 19:33:29', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DEDUPTHREAD '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW BANNER '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW RESQUEUE '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW TXNTABLE LOCKDETAIL=NO '], ['09/26/2022 19:33:29', 'ANR2034E QUERY MOUNT: No match found using this criteria. '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW SESSION FORMAT=DETAILED '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW THREADS '], ['09/26/2022 19:33:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW JVM '], ['09/26/2022 19:37:25', 'ANR8592I Session 851 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 851)'], ['09/26/2022 19:37:25', 'ANR0407I Session 851 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:51514). (SESSION: 851)'], ['09/26/2022 19:37:39', 'ANR0482W Session 843 for node IBM-OC-USERTSM.USR (DSMAPI) terminated - idle for more than 15 minutes. (SESSION: 843)'], ['09/26/2022 19:38:01', 'ANR1959I Status monitor collecting current data at 07:38:01 PM. '], ['09/26/2022 19:38:07', 'ANR1960I Status monitor finished collecting data at 07:38:07 PM and will sleep for 10 minutes. '], ['09/26/2022 19:38:55', 'ANR0405I Session 845 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 845)'], ['09/26/2022 19:42:20', 'ANR3638W Space reclamation skipped volume USER08L4 because the spanned volume SA1797L4 in storage pool FILES_LTO is inaccessible. '], ['09/26/2022 19:42:25', 'ANR8592I Session 853 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 853)'], ['09/26/2022 19:42:25', 'ANR0407I Session 853 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:46576). (SESSION: 853)'], ['09/26/2022 19:43:26', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW ALLOC '], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW REPLICATION '], ['09/26/2022 19:43:27', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS '], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW CLOUDREADCACHE '], ['09/26/2022 19:43:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DBSPACE' order by COLNO -comma "], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DBSPACE -comma '], ['09/26/2022 19:43:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='LOG' order by COLNO -comma "], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM LOG -comma '], ['09/26/2022 19:43:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DEVCLASSES' order by COLNO -comma "], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DEVCLASSES -comma '], ['09/26/2022 19:43:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DEVCLASSES_DIR' order by COLNO -comma "], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DEVCLASSES_DIR -comma '], ['09/26/2022 19:43:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='STGPOOLS' order by COLNO -comma "], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM STGPOOLS -comma '], ['09/26/2022 19:43:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='STGPOOL_DIRS' order by COLNO -comma "], ['09/26/2022 19:43:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM STGPOOL_DIRS -comma '], ['09/26/2022 19:43:27', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 19:43:27', 'ANR2034E SELECT: No match found using this criteria. '], ['09/26/2022 19:43:28', 'ANR0944E QUERY PROCESS: No active processes found. '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS ONLYWAITERS=YES '], ['09/26/2022 19:43:28', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 19:43:28', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DEDUPTHREAD '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW BANNER '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW RESQUEUE '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW TXNTABLE LOCKDETAIL=NO '], ['09/26/2022 19:43:28', 'ANR2034E QUERY MOUNT: No match found using this criteria. '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW SESSION FORMAT=DETAILED '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW THREADS '], ['09/26/2022 19:43:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW JVM '], ['09/26/2022 19:43:40', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DBCONN '], ['09/26/2022 19:47:25', 'ANR8592I Session 855 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 855)'], ['09/26/2022 19:47:25', 'ANR0407I Session 855 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:49308). (SESSION: 855)'], ['09/26/2022 19:48:01', 'ANR1959I Status monitor collecting current data at 07:48:01 PM. '], ['09/26/2022 19:48:05', 'ANR1960I Status monitor finished collecting data at 07:48:05 PM and will sleep for 10 minutes. '], ['09/26/2022 19:50:55', 'ANR0405I Session 851 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 851)'], ['09/26/2022 19:51:05', 'ANR8592I Session 856 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 856)'], ['09/26/2022 19:51:05', 'ANR0406I Session 856 started for node SP_VE_VMCLI (TDP VMware) (SSL tsm.in.useribm.hu[10.228.109.249]:35946). (SESSION: 856)'], ['09/26/2022 19:51:05', 'ANR0403I Session 856 ended for node SP_VE_VMCLI (TDP VMware). (SESSION: 856)'], ['09/26/2022 19:51:06', 'ANR8592I Session 857 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 857)'], ['09/26/2022 19:51:06', 'ANR0406I Session 857 started for node SP_VE_VMCLI (TDP VMware) (SSL tsm.in.useribm.hu[10.228.109.249]:35956). (SESSION: 857)'], ['09/26/2022 19:51:06', 'ANR0397I Session 857 for node SP_VE_VMCLI has begun a proxy session for node SP_VE_DATACENTER.  (SESSION: 857)'], ['09/26/2022 19:51:07', 'ANR0399I Session 857 for node SP_VE_VMCLI has ended a proxy session for node SP_VE_DATACENTER.  (SESSION: 857)'], ['09/26/2022 19:51:07', 'ANR0403I Session 857 ended for node SP_VE_VMCLI (TDP VMware). (SESSION: 857)'], ['09/26/2022 19:52:25', 'ANR8592I Session 859 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 859)'], ['09/26/2022 19:52:25', 'ANR0407I Session 859 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:53482). (SESSION: 859)'], ['09/26/2022 19:53:28', 'ANR0944E QUERY PROCESS: No active processes found. '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS ONLYWAITERS=YES '], ['09/26/2022 19:53:28', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 19:53:28', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DEDUPTHREAD '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW BANNER '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW RESQUEUE '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW TXNTABLE LOCKDETAIL=NO '], ['09/26/2022 19:53:28', 'ANR2034E QUERY MOUNT: No match found using this criteria. '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW SESSION FORMAT=DETAILED '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW THREADS '], ['09/26/2022 19:53:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW JVM '], ['09/26/2022 19:56:55', 'ANR0405I Session 853 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 853)'], ['09/26/2022 19:57:26', 'ANR8592I Session 861 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 861)'], ['09/26/2022 19:57:26', 'ANR0407I Session 861 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:60430). (SESSION: 861)'], ['09/26/2022 19:58:02', 'ANR1959I Status monitor collecting current data at 07:58:02 PM. '], ['09/26/2022 19:58:06', 'ANR1960I Status monitor finished collecting data at 07:58:06 PM and will sleep for 10 minutes. '], ['09/26/2022 20:00:01', 'ANR2561I Schedule prompter contacting SP_VE_DATACENTER_DM (session 862) to start a scheduled operation. (SESSION: 15)'], ['09/26/2022 20:00:01', 'ANR0403I Session 862 ended for node SP_VE_DATACENTER_DM (). (SESSION: 15)'], ['09/26/2022 20:00:04', 'ANR8592I Session 863 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 863)'], ['09/26/2022 20:00:04', 'ANR0406I Session 863 started for node SP_VE_DATACENTER_DM (TDP VMware) (SSL localhost[127.0.0.1]:39128). (SESSION: 863)'], ['09/26/2022 20:00:04', 'ANR0397I Session 863 for node SP_VE_DATACENTER_DM has begun a proxy session for node SP_VE_DATACENTER.  (SESSION: 863)'], ['09/26/2022 20:00:04', 'ANE4917E (Session: 863, Node: SP_VE_DATACENTER)  A failure occurred while accessing the VMware libraries. The required files for the virtual machine backup were not found. The files are installed only if the client is defined as a data mover in IBM Spectrum Protect for Virtual Environments.  (SESSION: 863)'], ['09/26/2022 20:00:04', 'ANR0399I Session 863 for node SP_VE_DATACENTER_DM has ended a proxy session for node SP_VE_DATACENTER.  (SESSION: 863)'], ['09/26/2022 20:00:04', 'ANR0403I Session 863 ended for node SP_VE_DATACENTER_DM (TDP VMware). (SESSION: 863)'], ['09/26/2022 20:02:25', 'ANR8592I Session 865 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 865)'], ['09/26/2022 20:02:25', 'ANR0407I Session 865 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:53608). (SESSION: 865)'], ['09/26/2022 20:02:40', 'ANR0482W Session 855 for node IBM-OC-USERTSM.USR (DSMAPI) terminated - idle for more than 15 minutes. (SESSION: 855)'], ['09/26/2022 20:03:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DBSPACE' order by COLNO -comma "], ['09/26/2022 20:03:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DBSPACE -comma '], ['09/26/2022 20:03:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='LOG' order by COLNO -comma "], ['09/26/2022 20:03:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM LOG -comma '], ['09/26/2022 20:03:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DEVCLASSES' order by COLNO -comma "], ['09/26/2022 20:03:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DEVCLASSES -comma '], ['09/26/2022 20:03:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DEVCLASSES_DIR' order by COLNO -comma "], ['09/26/2022 20:03:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DEVCLASSES_DIR -comma '], ['09/26/2022 20:03:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='STGPOOLS' order by COLNO -comma "], ['09/26/2022 20:03:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM STGPOOLS -comma '], ['09/26/2022 20:03:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='STGPOOL_DIRS' order by COLNO -comma "], ['09/26/2022 20:03:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM STGPOOL_DIRS -comma '], ['09/26/2022 20:03:27', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 20:03:27', 'ANR2034E SELECT: No match found using this criteria. '], ['09/26/2022 20:03:28', 'ANR0944E QUERY PROCESS: No active processes found. '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS ONLYWAITERS=YES '], ['09/26/2022 20:03:28', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 20:03:28', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DEDUPTHREAD '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW BANNER '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW RESQUEUE '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW TXNTABLE LOCKDETAIL=NO '], ['09/26/2022 20:03:28', 'ANR2034E QUERY MOUNT: No match found using this criteria. '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW SESSION FORMAT=DETAILED '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW THREADS '], ['09/26/2022 20:03:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW JVM '], ['09/26/2022 20:03:40', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DBCONN '], ['09/26/2022 20:07:25', 'ANR8592I Session 867 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 867)'], ['09/26/2022 20:07:25', 'ANR0407I Session 867 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:39778). (SESSION: 867)'], ['09/26/2022 20:07:26', 'ANR0482W Session 859 for node IBM-OC-USERTSM.USR (DSMAPI) terminated - idle for more than 15 minutes. (SESSION: 859)'], ['09/26/2022 20:07:26', 'ANR0405I Session 867 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 867)'], ['09/26/2022 20:08:02', 'ANR1959I Status monitor collecting current data at 08:08:02 PM. '], ['09/26/2022 20:08:06', 'ANR1960I Status monitor finished collecting data at 08:08:06 PM and will sleep for 10 minutes. '], ['09/26/2022 20:08:55', 'ANR0405I Session 861 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 861)'], ['09/26/2022 20:11:04', 'ANR8592I Session 868 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 868)'], ['09/26/2022 20:11:04', 'ANR0406I Session 868 started for node SP_VE_VMCLI (TDP VMware) (SSL tsm.in.useribm.hu[10.228.109.249]:34982). (SESSION: 868)'], ['09/26/2022 20:11:05', 'ANR0403I Session 868 ended for node SP_VE_VMCLI (TDP VMware). (SESSION: 868)'], ['09/26/2022 20:11:06', 'ANR8592I Session 869 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 869)'], ['09/26/2022 20:11:06', 'ANR0406I Session 869 started for node SP_VE_VMCLI (TDP VMware) (SSL tsm.in.useribm.hu[10.228.109.249]:34984). (SESSION: 869)'], ['09/26/2022 20:11:06', 'ANR0397I Session 869 for node SP_VE_VMCLI has begun a proxy session for node SP_VE_DATACENTER.  (SESSION: 869)'], ['09/26/2022 20:11:07', 'ANR0399I Session 869 for node SP_VE_VMCLI has ended a proxy session for node SP_VE_DATACENTER.  (SESSION: 869)'], ['09/26/2022 20:11:07', 'ANR0403I Session 869 ended for node SP_VE_VMCLI (TDP VMware). (SESSION: 869)'], ['09/26/2022 20:12:26', 'ANR8592I Session 871 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 871)'], ['09/26/2022 20:12:26', 'ANR0407I Session 871 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:41278). (SESSION: 871)'], ['09/26/2022 20:12:50', 'ANR0406I Session 872 started for node TFS (WinNT) (Tcp/Ip tfs.sr.user.hu[192.168.42.51]:62799). (SESSION: 872)'], ['09/26/2022 20:12:50', 'ANR0403I Session 872 ended for node TFS (WinNT). (SESSION: 872)'], ['09/26/2022 20:12:52', 'ANR0406I Session 873 started for node TFS (WinNT) (Tcp/Ip tfs.sr.user.hu[192.168.42.51]:62803). (SESSION: 873)'], ['09/26/2022 20:12:55', 'ANR0406I Session 874 started for node TFS_SQL (TDP MSSQL Win64) (Tcp/Ip tfs.sr.user.hu[192.168.42.51]:62806). (SESSION: 874)'], ['09/26/2022 20:12:56', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3006 Data Protection for SQL: Starting backup for server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:12:56', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3000 Data Protection for SQL: Starting full backup of database master from server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:12:57', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3001 Data Protection for SQL: full backup of database master from server TFS\\SQLEXPRESS completed successfully. (SESSION: 874)'], ['09/26/2022 20:12:57', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3000 Data Protection for SQL: Starting full backup of database model from server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:12:58', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3001 Data Protection for SQL: full backup of database model from server TFS\\SQLEXPRESS completed successfully. (SESSION: 874)'], ['09/26/2022 20:12:58', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3000 Data Protection for SQL: Starting full backup of database msdb from server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:12:59', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3001 Data Protection for SQL: full backup of database msdb from server TFS\\SQLEXPRESS completed successfully. (SESSION: 874)'], ['09/26/2022 20:12:59', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3000 Data Protection for SQL: Starting full backup of database Tfs_Configuration from server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:13:00', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3001 Data Protection for SQL: full backup of database Tfs_Configuration from server TFS\\SQLEXPRESS completed successfully. (SESSION: 874)'], ['09/26/2022 20:13:00', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3000 Data Protection for SQL: Starting full backup of database Tfs_Cooperation from server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:13:28', 'ANR0944E QUERY PROCESS: No active processes found. '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS ONLYWAITERS=YES '], ['09/26/2022 20:13:28', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 20:13:28', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DEDUPTHREAD '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW BANNER '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW RESQUEUE '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW TXNTABLE LOCKDETAIL=NO '], ['09/26/2022 20:13:28', 'ANR2034E QUERY MOUNT: No match found using this criteria. '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW SESSION FORMAT=DETAILED '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW THREADS '], ['09/26/2022 20:13:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW JVM '], ['09/26/2022 20:13:32', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3001 Data Protection for SQL: full backup of database Tfs_Cooperation from server TFS\\SQLEXPRESS completed successfully. (SESSION: 874)'], ['09/26/2022 20:13:32', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3000 Data Protection for SQL: Starting full backup of database Tfs_DefaultCollection from server TFS\\SQLEXPRESS. (SESSION: 874)'], ['09/26/2022 20:14:55', 'ANR0405I Session 865 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 865)'], ['09/26/2022 20:15:09', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3001 Data Protection for SQL: full backup of database Tfs_DefaultCollection from server TFS\\SQLEXPRESS completed successfully. (SESSION: 874)'], ['09/26/2022 20:15:10', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO3008 Data Protection for SQL: Backup of server TFS\\SQLEXPRESS is complete.  Total SQL backups selected:               6  Total SQL backups attempted:              6  Total SQL backups completed:              6  Total SQL backups excluded:               0  Total SQL backups inactivated:            0  Throughput rate:                          93,711.68 Kb/Sec  Total bytes transferred:                  12,811,529,728  Elapsed processing time:                  133.51 Secs (SESSION: 874)'], ['09/26/2022 20:15:10', 'ANE4991I (Session: 874, Node: TFS_SQL)  TDP MSSQL Win64 ACO5195 Data Protection for SQL: Backup of server TFS\\SQLEXPRESS enhanced statistics.  Total SQL backups deduplicated:           0  Throughput rate:                          93,711.68 Kb/Sec  Total bytes inspected:                    12,811,529,728  Total bytes transferred:                  12,811,529,728  Total LanFree bytes transferred:          0  Total bytes before deduplication:         0  Total bytes after deduplication:          0  Data compressed by:                       0%  Deduplication reduction:                  0.00%  Total data reduction ratio:               0.00%  Elapsed processing time:                  133.51 Secs (SESSION: 874)'], ['09/26/2022 20:15:10', 'ANR0403I Session 874 ended for node TFS_SQL (TDP MSSQL Win64). (SESSION: 874)'], ['09/26/2022 20:15:11', 'ANR2507I Schedule SQL_2000 for domain FILES started at 09/26/2022 08:00:00 PM for node TFS completed successfully at 09/26/2022 08:15:11 PM. (SESSION: 873)'], ['09/26/2022 20:15:11', 'ANR0403I Session 873 ended for node TFS (WinNT). (SESSION: 873)'], ['09/26/2022 20:15:11', 'ANR0406I Session 875 started for node TFS (WinNT) (Tcp/Ip tfs.sr.user.hu[192.168.42.51]:62824). (SESSION: 875)'], ['09/26/2022 20:15:11', 'ANR0403I Session 875 ended for node TFS (WinNT). (SESSION: 875)'], ['09/26/2022 20:17:25', 'ANR8592I Session 877 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 877)'], ['09/26/2022 20:17:25', 'ANR0407I Session 877 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:40532). (SESSION: 877)'], ['09/26/2022 20:18:02', 'ANR1959I Status monitor collecting current data at 08:18:02 PM. '], ['09/26/2022 20:18:06', 'ANR1960I Status monitor finished collecting data at 08:18:06 PM and will sleep for 10 minutes. '], ['09/26/2022 20:20:04', 'ANR8592I Session 878 connection is using protocol TLSV13, cipher specification TLS_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 878)'], ['09/26/2022 20:20:04', 'ANR0406I Session 878 started for node SP_VE_DATACENTER_DM (TDP VMware) (SSL localhost[127.0.0.1]:59434). (SESSION: 878)'], ['09/26/2022 20:20:04', 'ANR0397I Session 878 for node SP_VE_DATACENTER_DM has begun a proxy session for node SP_VE_DATACENTER.  (SESSION: 878)'], ['09/26/2022 20:20:04', 'ANE4917E (Session: 878, Node: SP_VE_DATACENTER)  A failure occurred while accessing the VMware libraries. The required files for the virtual machine backup were not found. The files are installed only if the client is defined as a data mover in IBM Spectrum Protect for Virtual Environments.  (SESSION: 878)'], ['09/26/2022 20:20:04', 'ANR0399I Session 878 for node SP_VE_DATACENTER_DM has ended a proxy session for node SP_VE_DATACENTER.  (SESSION: 878)'], ['09/26/2022 20:20:04', 'ANR0403I Session 878 ended for node SP_VE_DATACENTER_DM (TDP VMware). (SESSION: 878)'], ['09/26/2022 20:22:25', 'ANR8592I Session 880 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 880)'], ['09/26/2022 20:22:25', 'ANR0407I Session 880 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:60430). (SESSION: 880)'], ['09/26/2022 20:23:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DBSPACE' order by COLNO -comma "], ['09/26/2022 20:23:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DBSPACE -comma '], ['09/26/2022 20:23:27', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='LOG' order by COLNO -comma "], ['09/26/2022 20:23:27', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM LOG -comma '], ['09/26/2022 20:23:28', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DEVCLASSES' order by COLNO -comma "], ['09/26/2022 20:23:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DEVCLASSES -comma '], ['09/26/2022 20:23:28', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='DEVCLASSES_DIR' order by COLNO -comma "], ['09/26/2022 20:23:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM DEVCLASSES_DIR -comma '], ['09/26/2022 20:23:28', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='STGPOOLS' order by COLNO -comma "], ['09/26/2022 20:23:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM STGPOOLS -comma '], ['09/26/2022 20:23:28', "ANR2017I Administrator SERVER_CONSOLE issued command: select colname,'' from syscat.columns where tabname='STGPOOL_DIRS' order by COLNO -comma "], ['09/26/2022 20:23:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SELECT * FROM STGPOOL_DIRS -comma '], ['09/26/2022 20:23:28', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 20:23:28', 'ANR2034E SELECT: No match found using this criteria. '], ['09/26/2022 20:23:28', 'ANR0944E QUERY PROCESS: No active processes found. '], ['09/26/2022 20:23:28', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW LOCKS ONLYWAITERS=YES '], ['09/26/2022 20:23:28', 'ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria. '], ['09/26/2022 20:23:29', 'ANR2034E QUERY REPLICATION: No match found using this criteria. '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DEDUPTHREAD '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW BANNER '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW RESQUEUE '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW TXNTABLE LOCKDETAIL=NO '], ['09/26/2022 20:23:29', 'ANR2034E QUERY MOUNT: No match found using this criteria. '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW SESSION FORMAT=DETAILED '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW THREADS '], ['09/26/2022 20:23:29', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW JVM '], ['09/26/2022 20:23:41', 'ANR2017I Administrator SERVER_CONSOLE issued command: SHOW DBCONN '], ['09/26/2022 20:26:55', 'ANR0405I Session 871 ended for administrator IBM-OC-USERTSM.USR (DSMAPI). (SESSION: 871)'], ['09/26/2022 20:27:25', 'ANR8592I Session 882 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 882)'], ['09/26/2022 20:27:25', 'ANR0407I Session 882 started for administrator IBM-OC-USERTSM.USR (DSMAPI) (SSL localhost[127.0.0.1]:52752). (SESSION: 882)'], ['09/26/2022 20:27:26', 'ANR8592I Session 883 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 883)'], ['09/26/2022 20:27:26', 'ANR0407I Session 883 started for administrator SUPPORT (Mac) (SSL 172.16.223.14:63757). (SESSION: 883)'], ['09/26/2022 20:27:26', 'ANR2017I Administrator SUPPORT issued command: QUERY NODE Help!  (SESSION: 883)'], ['09/26/2022 20:27:26', 'ANR3571E QUERY NODE: The node_name parameter value HELP! contains an invalid character "!". The following characters are valid: "*?ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-+&@" (excluding the quotation marks). (SESSION: 883)'], ['09/26/2022 20:27:26', 'ANR3589I QUERY NODE: For more information, issue the HELP QUERY NODE command. (SESSION: 883)'], ['09/26/2022 20:27:26', 'ANR2017I Administrator SUPPORT issued command: ROLLBACK  (SESSION: 883)'], ['09/26/2022 20:27:28', 'ANR0405I Session 883 ended for administrator SUPPORT (Mac). (SESSION: 883)'], ['09/26/2022 20:27:33', 'ANR8592I Session 884 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 884)'], ['09/26/2022 20:27:33', 'ANR0407I Session 884 started for administrator SUPPORT (Mac) (SSL 172.16.223.14:63758). (SESSION: 884)'], ['09/26/2022 20:27:33', 'ANR2017I Administrator SUPPORT issued command: select SERVER_NAME from STATUS (SESSION: 884)'], ['09/26/2022 20:27:33', 'ANR2017I Administrator SUPPORT issued command: select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS (SESSION: 884)'], ['09/26/2022 20:27:36', 'ANR2017I Administrator SUPPORT issued command: select STGPOOL_NAME,DEVCLASS,COLLOCATE,EST_CAPACITY_MB,PCT_UTILIZED,PCT_MIGR,HIGHMIG,LOWMIG,RECLAIM,NEXTSTGPOOL from STGPOOLS (SESSION: 884)'], ['09/26/2022 20:27:36', 'ANR0568W Session 884 for admin SUPPORT (Mac) terminated - connection with client severed. (SESSION: 884)'], ['09/26/2022 20:28:03', 'ANR1959I Status monitor collecting current data at 08:28:03 PM. '], ['09/26/2022 20:28:07', 'ANR8592I Session 885 connection is using protocol TLSV12, cipher specification TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, certificate TSM Self-Signed Certificate.  (SESSION: 885)'], ['09/26/2022 20:28:07', 'ANR0407I Session 885 started for administrator SUPPORT (Mac) (SSL 172.16.223.14:63760). (SESSION: 885)'], ['09/26/2022 20:28:07', 'ANR2017I Administrator SUPPORT issued command: select SERVER_NAME from STATUS (SESSION: 885)'], ['09/26/2022 20:28:07', 'ANR1960I Status monitor finished collecting data at 08:28:07 PM and will sleep for 10 minutes. '], ['09/26/2022 20:28:07', 'ANR2017I Administrator SUPPORT issued command: select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS (SESSION: 885)'], ['09/26/2022 20:28:10', 'ANR2017I Administrator SUPPORT issued command: QUERY ACTLOG  (SESSION: 885)']]
sess_data = [[1, '13', 'Run', '0', '2 MiB', '62 KiB', 'Admin', 'DSMAPI', 'IBM-OC-USERTSM.USR', '', 'RecvPing'], [2, '14', 'IdleW', '\x1b[1m\x1b[31m222\x1b[0m', '5 MiB', '3 MiB', 'Admin', 'DSMAPI', 'IBM-OC-USERTSM.USR', '', 'SentAdmCmdResp'], [3, '1506', 'IdleW', '\x1b[1m\x1b[31m222\x1b[0m', '475 KiB', '329 KiB', 'Admin', 'DSMAPI', 'IBM-OC-USERTSM.USR', '', 'SentAdmCmdResp'], [4, '1796', 'IdleW', '\x1b[1m\x1b[31m550\x1b[0m', '165 B', '204 B', 'Admin', 'DSMAPI', 'IBM-OC-USERTSM.USR', '', 'SentTimeQryResp'], [5, '1800', 'IdleW', '\x1b[1m\x1b[31m250\x1b[0m', '165 B', '204 B', 'Admin', 'DSMAPI', 'IBM-OC-USERTSM.USR', '', 'SentTimeQryResp'], [6, '1801', 'Run', '0', '309 B', '654 B', 'Admin', 'Mac', 'SUPPORT', '', 'RecvAdmCmd']]


table = columnar(actlog_data, headers=['Date/Time', 'Message'], justify=['l', 'l'])
print(table)

table = columnar(stgp_data, headers=['PoolName', 'DeviceClass', 'Coll', 'EstCap', 'PctUtil', 'PctMigr', 'HighMig', 'LowMig',
                                'Recl', 'Next'],
                 justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])
print(table)


table = columnar(sess_data, headers = [
        '#', 'Id', 'State', 'Wait', 'Sent', 'Received', 'Type', 'Platform', 'Name', 'MediaAccess', 'Verb' ],
        justify=[ 'r', 'c', 'c', 'r', 'r', 'r', 'r', 'c', 'l', 'l', 'l' ])

print(table)
