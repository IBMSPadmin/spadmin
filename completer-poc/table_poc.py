import columnar
from click import style

data = [['ABEL', 'Mac', 'FILES', '1,675', '1,740', 'No'], ['ACCOUNTING', 'WinNT', 'FILES', '1,036', '1,123', 'No'],
        ['ADS', 'WinNT', 'FILES', '<1', '59', 'No'], ['AIAC922', 'LinuxPPC64LE', 'FILES', '950', '977', 'No'],
        ['AKMINECRAFT', 'Linux x86-64', 'FILES', '674', '761', 'No'],
        ['ASSZISZTENCIA', 'WinNT', 'FILES', '687', '212', 'No'], ['CDS822', 'LinuxPPC64', 'FILES', '941', '949', 'No'],
        ['CSABA_GEPE', 'WinNT', 'FILES', '1,319', '1,577', 'No'],
        ['CVMB.USR.USER.HU', 'Linux x86-64', 'FILES', '1,442', '1,486', 'No'],
        ['DB2RHEL5', 'Linux x86-64', 'FILES', '<1', '68', 'No'],
        ['DB2SVR.USR', 'Linux x86-64', 'FILES', '<1', '61', 'No'],
        ['DB2SVR_DB2.USR', 'DB2/LINUXX8664', 'DB2', '28', '46', 'No'],
        ['DESKTOP-OHVBRDI', 'WinNT', 'FILES', '14', '17', 'No'], ['DEV2008', 'WinNT', 'FILES', '<1', '57', 'No'],
        ['DOMINO', 'Linux86', 'FILES', '1,898', '2,593', 'No'],
        ['ELGEKKO', 'WinNT', 'STANDARD', '1,290', '1,290', 'No'],
        ['FDTHINKSTATION', 'Linux x86-64', 'FILES', '78', '79', 'No'],
        ['FPGADEV', 'Linux x86-64', 'FILES', '78', '79', 'No'], ['HAJNALKA', 'Mac', 'FILES', '255', '255', 'No'],
        ['IBM_DEPLOY_CLIENT_MAC', '(?)', 'IBM_DEPLOY_CLIENT', '210', '17', 'No'],
        ['IBM_DEPLOY_CLIENT_UNX', '(?)', 'IBM_DEPLOY_CLIENT', '210', '2', 'No'],
        ['IBM_DEPLOY_CLIENT_WIN', '(?)', 'IBM_DEPLOY_CLIENT', '210', '17', 'No'],
        ['KALMAN_NOTEBOOK', 'WinNT', 'FILES', '722', '722', 'No'], ['KARCSIMAC', 'Mac', 'FILES', '311', '311', 'No'],
        ['KOFAX1', 'WinNT', 'FILES', '92', '92', 'No'], ['KOFAX2', 'WinNT', 'FILES', '254', '254', 'No'],
        ['KOFAX_CLUSTER', 'WinNT', 'FILES', '554', '561', 'No'],
        ['MEDIACUBE', 'WinNT', 'MEDIACUBE', '200', '273', 'No'], ['RTC', 'Linux x86-64', 'FILES', '29', '44', 'No'],
        ['SLC-INS5558-KVA', 'WinNT', 'FILES', '72', '72', 'No'],
        ['SP_VE_DATACENTER', 'TDP VMware', 'VMWARE', '1', '685', 'No'],
        ['SP_VE_DATACENTER_DM', 'TDP VMware', 'VMWARE', '1', '53', 'No'],
        ['SP_VE_REMOTE_MP_LNX', '(?)', 'VMWARE', '1,019', '1,019', 'No'],
        ['SP_VE_REMOTE_MP_WIN', '(?)', 'VMWARE', '1,019', '1,019', 'No'],
        ['SP_VE_VCENTER', '','VMWARE', '1,047', '1,200', 'No'], ['SP_VE_VMCLI', 'TDP VMware', 'VMWARE', '10', '269', 'No'],
        ['STORE.USR', 'Linux x86-64', 'FILES', '1', '49', 'No'],
        ['STORE_03', 'Mac', 'STORE_03_DOMAIN', '584', '2,186', 'No'],
        ['SVC.PM', 'TDP VMware', 'FILES', '1,513', '1,513', 'No'], ['TFS', 'WinNT', 'FILES', '<1', '62', 'No'],
        ['TFS_SQL', 'TDP MSSQL Win64', 'SQL', '1', '44', 'No'],
        ['THINK', 'Linux x86-64', 'FILES', '1,369', '1,369', 'No'], ['TOMBOR-PC', 'WinNT', 'FILES', '485', '485', 'No'],
        ['TSMAPI', 'UBIS_TSM_API', 'TSMAPI', '1,879', '2,326', 'Yes'],
        ['U200', 'Linux x86-64', 'FILES', '46', '83', 'No'], ['USERTSM.USR', 'TDP VMware', 'FILES', '1', '53', 'No'],
        ['VHOST1', 'Linux x86-64', 'FILES', '1', '8', 'No'], ['VHOST2', 'Linux x86-64', 'FILES', '1', '37', 'No'],
        ['WASRHEL5', 'Linux x86-64', 'FILES', '<1', '68', 'No'], ['WORKSHEET', 'Linux86', 'FILES', '766', '788', 'No'],
        ['WSHEET_DB2', 'DB2/LINUXX8664', 'DB2', '766', '790', 'No']]

patterns = [
    ('Saturday.+', lambda text: style(text, fg='white', bg='blue')),
    ('\d+km', lambda text: style(text, fg='cyan')),
    ('Omloop Het Nieuwsblad', lambda text: style(text, fg='green')),
    ('Strade Bianche', lambda text: style(text, fg='white')),
    ('Milan-San Remo', lambda text: style(text, fg='red')),
    ('Tour of Flanders', lambda text: style(text, fg='yellow')),
]

columnar = columnar.Columnar()

table = columnar(data, headers=['Race', 'Date', 'Location', 'Distance'], patterns=patterns, no_borders=True)
print(table)
