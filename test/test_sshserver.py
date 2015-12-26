#make import
import sys, threading, socket, paramiko

#information about user
usern = "dadl"
passwd = "dadl"

#server builder
class Server(paramiko.ServerInterface):
    #initialize build
    def __init__ (self):
        self.event = threading.Event()
    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return(paramiko.OPEN_SUCCEEDED)
        return(paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED)
    #check password
    def check_auth_password(self, username, password):
        if (username == usern) and (password == passwd):
            return(paramiko.AUTH_SUCCESSFUL)
        return(paramiko.AUTH_FAILED)

#main loop
def looper(ip, port, key, keypassword):
    #create sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #set ssh options for socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #bind socket
    try:
        sock.bind((ip, port))
    except:
        print("error : UNABLE TO BIND SOCKET AT " + str(ip) + ":" + str(port))
        sys.exit()
    #begin listening 
    sock.listen(20)
    print("[*] listening . . . \n")
    while True:
        #connect to client and get address
        try:
            (client, addr) = sock.accept()
            print("[+] connected to " + addr[0])
        except:
            print("error : CANNOT CONNECT TO CLIENT")
            sys.exit()
        #transport client to paramiko and add server key
        try:
            session = paramiko.Transport(client)
            paramiko.util.log_to_file("test.log")
            session.add_server_key(paramiko.RSAKey(filename=key, password=keypassword))
        except:
            print("error : UNABLE TO TRANPORT CLIENT AND//OR ADD SERVER KEY")
            sys.exit()
        #create server instance
        server = Server()
        #start server that we have just created
        try:
            session.start_server(server=server)
        except:
            print("error : CANNOT START SERVER")
            sys.exit()
        #create channel
        channel = session.accept()
        print("[*] authenticated")
        #get data from client
        print("[==>] receiving data from client : ")
        data = channel.recv(1024)
        #print('Data received: %s'%data)
        #data.strip()
        print(data.decode("utf-8"))
        #send echo to client
        print("[<==] sending echo to client")
        channel.send('Data: %s'%data)
        print(data.decode("utf-8"))
        #close session
        session.close()

#cmd line parser
def main():
    #fancy cmd line parsing
#     if (len(sys.argv[1:]) != 4) and (len(sys.argv[1:]) != 3):
#         print("SSH SERVER\nCREATED BY BENDACODER")
#         print("USAGE : \n./SSHserver.py [serverIP] [serverPort] [sshKey] [sshKeyPswd]=optional")
#         sys.exit()
#     ip = sys.argv[1]
#     port = int(sys.argv[2])
#     key = sys.argv[3]
#     try:
#         pswd = sys.argv[4]
#     except:
#         pswd = None
    pswd = None
    ip, port, key = 'localhost', 21567, 'C:\Users\SouthParkKyle\gitCode\.ssh\id_rsa'
    looper(ip, port, key, pswd)

#execute in cmd
main()