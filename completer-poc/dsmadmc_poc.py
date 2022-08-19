import pexpect
import time

class DSM:
    START_DSMADMC = "dsmadmc"
    id = "support"
    pa = "userkft1q2"
    STARTCOMMAND = START_DSMADMC + " -id=" + id + " -pa=" + pa + " -dataonly=yes" + " -comma"
    MORE1 = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    MORE3 = 'Do you wish to proceed\? \(Yes \(Y\)/No \(N\)\)'  # meg itt
    PROMPT1 = 'Protect: .*'
    PROMPT2 = 'tsm: .*'
    tsm = None

    def get_tsm(self):
        if self.tsm is None or not self.tsm.isalive:
            self.tsm = pexpect.spawn('%s' % self.STARTCOMMAND, encoding='utf-8', echo=False)
            self.tsm.setwinsize(65534, 65534)
            self.tsm.expect([self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF])
        return self.tsm

    def send_command(self, command):
        tsm = DSM.get_tsm(DSM)
        try:
            tsm.sendline(command)
        except:
            print("An error occurred during a dsmadmc execution. Please try again...")
            quit(1)
        tsm.expect([self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF])
        return tsm.before

    def send_command_array(self, command):
        list = DSM.send_command(DSM,command).splitlines()
        if len(list) > 0:
            list.pop(0)  # delete the first line which is the command itself
        while ("" in list):  ## every output contains empty lines, we remove it
            list.remove("")
        return list


if __name__ == "__main__": ## Exception kezelés kell!!
    print("-------",DSM.send_command(DSM,"select SERVER_NAME from STATUS"),"-------")
    time.sleep(15)
    print("-------",DSM.send_command(DSM,"q node"),"-------")
    print("-------",DSM.send_command_array(DSM,"select DOMAIN_NAME from DOMAINS"),"-------")
    print("-------",DSM.send_command(DSM,"quit"), "-------")
