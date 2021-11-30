import paramiko
import time
import getpass

ip = '10.58.93.157'
un = 'root'
pw = 'arthur'

Session = False

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())


def start(un,pw,ip):
    global Session
    global client
    global sftp
    try :
        client.connect(hostname=ip,username=un, password=pw,timeout=1000)
        sftp = client.open_sftp()
        Session = True
        return Session, sftp
    except Exception as e:
        #client.close()
        print(e)
        Session=False
        return Session

def get_ftp(filepath,localpath):
    if Session:
         sftp.get(f'{filepath}',f'{localpath}')


def send_ftp(localpath,filepath,filename):
    if Session:
        sftp.put(f'{localpath+filename}',f'{filepath+filename}')



def SHELL(cmd):
    while Session:
        print('SHELL state: ', Session)
        key = True
        # cmd = input("Command to run: ")
        if cmd == "":
            break
        chan = client.get_transport().open_session()
        print("running '%s'" % cmd)
        chan.exec_command(cmd)
        while key:
            if chan.recv_ready():
                print("recv:\n%s" % chan.recv(4096).decode('ascii'))
            if chan.recv_stderr_ready():
                print("error:\n %s" % chan.recv_stderr(4096).decode())
            if chan.exit_status_ready():
                print("exit status: %s" % chan.recv_exit_status())
                key = False
                # client.close()

        return chan.recv_exit_status()
        # break



# X = start(un,pw,ip)
# Y = SHELL('ls -l')

# filename='username.txt'
# VM_path ='/opt/jetty/Mbackup/kkx/OMU/'
# local_path ='C:\\Users\\aelmaghrabi\PycharmProjects\Prototype\OSC_Demo\\'
#
# start(un,pw,ip)
# # sftp.get(VM_path,local_path)
# # SHELL(f'rm {VM_path+filename}')
# send_ftp(local_path,VM_path,filename)

