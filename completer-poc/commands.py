class SpadminCommand:
    def __init__(self):
        self.command_string = ""
        self.command_type = ""
        self.command_index = 0

    def get_command_string(self):
        return self.command_string

    def get_command_type(self):
        return self.command_type

    def get_command_index(self):
        return self.get_command_index

    def short_help(self) -> str:
        return 'Short description of command'

    def help(self) -> str:
        return """
Detailed description of command
with many lines
"""

    def _execute(self, parameters: str) -> str:
        return "not defined: " + parameters

    def execute(self, dummy, parameters):
        if parameters == "help":
            print(self.help())
        else:
            print(self._execute(parameters))


class ShowStgp(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow STGpools"
        self.command_type = "STGP"
        self.command_index = 0

    def short_help(self) -> str:
        return 'SHow STGpools: display information about storage pools'

    def help(self) -> dict:
        return """Display the following information about storage pools in the following order and format:
 - Storage Pool name               
 - Device Class name              
 - Collocation   
 - Estimated Capacity 
 - Percent Utilized 
 - Percent Migrate 
 - High Migration threshold 
 - Low Migration threshold 
 - Reclamation
 - Next Storage Pool name
        """

    def _execute(self, parameters: str) -> str:
        return """---------------------- ------------------------ ----- ------- ------- ------- ------- ------ ---- ----------
PoolName               DeviceClass              Coll   EstCap PctUtil PctMigr HighMig LowMig Recl Next
---------------------- ------------------------ ----- ------- ------- ------- ------- ------ ---- ----------
DB2_DSK                DISK                               0 B     0.0     0.0      80     20      DB2_LTO
DB2_LTO                DCLTO_01                 GROUP  18 TiB     0.0    40.0      80     70   60
FILES_CP               DCLTO_01C                NO      3 TiB     5.1                         100
FILES_DSK              DISK                             2 TiB    99.8     0.0      80     20      FILES_LTO
FILES_LTO              DCLTO_02                 GROUP  65 TiB    14.7    18.2      80     20   60
IBM_DEPLOY_CLIENT_POOL IBM_DEPLOY_CLIENT_IMPORT GROUP 100 GiB    10.0    10.0      90     70   60
VMWARE_CTL             DISK                            50 GiB    17.6    17.6      90     70
VMWARE_DSK             DISK                            10 TiB    76.4     0.0      80     20      VMWARE_LTO
VMWARE_LTO             DCLTO_05                 GROUP  41 TiB    33.4    64.0      80     20   60"""

