# !/usr/bin/env python3

# Libraries
import errno
import os
import signal
import socket
import sys
import time

# ------------

class Server():
    def __init__(self):
        if (len(sys.argv) >= 3):  # make sure that user gives a port number
            try:  # make sure that the user gives a number
                minfolder= sys.argv[1][1:]
                try:
                    if len(sys.argv[1].split('/'))>2:
                        print("ERROR: multi folders aske to creates")
                        sys.exit()
                    if not os.path.exists(minfolder):
                        os.mkdir(minfolder)
                except:
                    print("ERROR: multi folders aske to creates")
                    sys.exit()

                if int(sys.argv[2]) > 1024:  # make sure that the port number above 1024
                    p = int(sys.argv[2])  # convert the number to integer
                else:
                    print("ERROR: The port Number must be greater than 1024")
                    sys.exit()
            except:
                print('ERROR: Something wrong ')
                sys.exit()
        else:
            print("ERROR: Msut supply at least 1 arguments \nUSAGE: " + sys.argv[0] + "/folder port number ")
            sys.exit()

        self.SERVER_ADDRESS = (self.HOST, self.PORT) = '', p
        self.REQUEST_QUEUE_SIZE = 1024
        self.Generator(minfolder)

    def DeadPool(signum, frame, temp):
        while True:
            try:
                pid, status = os.waitpid(
                    -1,  # Wait for any client to  process
                    os.WNOHANG  # Do not block and return EWOULDBLOCK error
                    # EWOULDBLOCK means that the socket send buffer is full when sending, or that the socket receive
                    # buffer is empty when receiving. You are supposed to use select() to detect when these conditions
                    # become false.
                )
            except OSError:
                return
                # The base class for the exceptions that are raised when a key or index used on a mapping or sequence
                # is invalid: IndexError , KeyError . This can be raised directly by codecs.lookup() . The base class
                # for exceptions that can occur outside the Python system: IOError , OSError .

            if pid == 0:  # no more dummy clients "zombies"
                return

                # Handling the request from the clients

    def WorkStation(self,minfolder):
        try:
            data = self.client.recv(1024)
            Line_1 = data.decode()
            comm = Line_1.split('|||')[0]
            if 'PUT' in comm:
                filename1 = Line_1.split('|||')[1]
                Fsize1 = int(Line_1.split('|||')[2])
                filename2 = Line_1.split('|||')[3]
                Fsize2 = int(Line_1.split('|||')[4])
                user= Line_1.split('|||')[5]
                password= Line_1.split('|||')[6]
                folder=Line_1.split('|||')[7]
                try:
                    with open ('dfs.conf','r') as fh:
                        conf=fh.read().split()
                except:
                    conf=['admin','admin123']
                Auth= False
                for i in range (len(conf)):
                    if user==conf[i] and password==conf[i+1]:
                        Auth=True
                        try:
                            os.mkdir(minfolder+'/'+user)
                        except:
                            pass
                        f=''
                        for i in range(len(folder.split('/'))):
                            if folder.split('/')[i]:
                                f+=folder.split('/')[i]+'/'
                                try:
                                    os.mkdir(minfolder+'/'+user+'/'+f)
                                except:
                                    pass

                        #try:
                            #os.mkdir('DFS1/'+user+folder)
                        #except:
                            #pass
                        try:
                            fh1 = open(minfolder+'/'+user +folder+'/'+filename1, 'wb')
                            fh2 = open(minfolder+'/'+user+folder+'/'+filename2, 'wb')
                            self.client.send(b'200 ready_to_receive')
                            c=0
                            while c<Fsize1:
                                # receive data from web server
                                data = self.client.recv(1024)
                                if (len(data) > 0):
                                    c+=1024
                                # send to browser
                                # self.client.send(data)
                                # http_response += data
                                    fh1.write(data)
                                else:
                                    break
                            self.client.send(b'200 ready_to_receive')
                            cc=0
                            while cc<Fsize2:
                                # receive data from web server
                                data = self.client.recv(1024)
                                if (len(data) > 0):
                                    c+=1024
                                        # send to browser
                                        # self.client.send(data)
                                        # http_response += data
                                    fh2.write(data)
                                else:
                                    break

                            fh1.close()
                            fh2.close()
                        except:
                            self.client.send(b'500 system fail.')
                    i+=2
                if not Auth:
                    self.client.send(b'400 Invalid Username/Password. Try again.')

                self.client.close()
                
            elif 'FIND' in comm:
                filename = Line_1.split('|||')[1]
                user= Line_1.split('|||')[2]
                password= Line_1.split('|||')[3]
                folder=Line_1.split('|||')[4]
                f=[]
                try:
                    with open ('dfs.conf','r') as fh:
                        conf=fh.read().split()
                except:
                    conf=['admin','admin123']
                Auth= False
                for i in range (len(conf)):
                    if user==conf[i] and password==conf[i+1]:
                        Auth= True
                        try:
                            for root, dirs, files in os.walk(minfolder+'/'+user+folder):
                                for i in range(5):
                                    if filename+'.P' + str(i) in files:
                                        f.append(filename+'.P' + str(i))
                            if len(f)==0:
                                self.client.send(b'404|||File does not exisit')
                                self.client.close()
                            else:
                                comms='200|||'
                                data=b''
                                for i in range(len(f)):
                                    comms+=f[i]+'|||'
                                    with open (minfolder+'/'+user+folder+'/'+f[i],'rb') as fh:
                                        data+=fh.read()
                                self.client.send(comms.encode())
                              
                        except:
                            self.client.send(b'404|||Folder does not exisit')
                            self.client.close()
                    i+=2
                if not Auth:
                    self.client.send(b'400 Invalid Username/Password. Try again.')
                    self.client.close()


            elif 'GET' in comm:
                filename = Line_1.split('|||')[1]
                user= Line_1.split('|||')[2]
                password= Line_1.split('|||')[3]
                folder=Line_1.split('|||')[4]
                f=[]
                try:
                    with open ('dfs.conf','r') as fh:
                        conf=fh.read().split()
                except:
                    conf=['admin','admin123']
                Auth= False
                for i in range (len(conf)):
                    if user==conf[i] and password==conf[i+1]:
                        Auth= True
                        try:
                            if os.path.isfile(minfolder+'/'+user+folder+'/'+filename):
                                comms=b'200|||'+str(os.path.getsize(minfolder+'/'+user+folder+'/'+filename)).encode()+b'||| ready to send the file'
                                self.client.send(comms)
                                data=self.client.recv(1024)
                                if data.decode().split('|||'):
                                    with open(minfolder+'/'+user+folder+'/'+filename, 'rb')as fh:
                                        data=fh.read()
                                    self.client.send(data)
                                    self.client.close()

                            else:
                                self.client.send(b'404|||File does not exisit')
                                self.client.close()
                        except:
                            self.client.send(b'404|||Folder does not exisit')
                            self.client.close()
                    i+=2

                if not Auth:
                    self.client.send(b'400 Invalid Username/Password. Try again.')
                    self.client.close()

            elif 'ROOT' in comm:
                filename = Line_1.split('|||')[1]
                user= Line_1.split('|||')[2]
                password= Line_1.split('|||')[3]
                folder=Line_1.split('|||')[4]
                f=[]
                try:
                    with open ('dfs.conf','r') as fh:
                        conf=fh.read().split()
                except:
                    conf=['admin','admin123']
                Auth= False
                for i in range (len(conf)):
                    if user==conf[i] and password==conf[i+1]:
                        Auth=True
                        try:
                            comms='200|||'
                            data=''
                            for root, dirs, files in os.walk(minfolder+'/'+user+folder):
                                comms+=root[5:]+'|||'


                                    
                            self.client.send(comms.encode())
                            self.client.close()
                        except:
                            self.client.send(b'404|||Folder does not exisit')
                            self.client.close()
                    i+=2

                if not Auth:
                    self.client.send(b'400 Invalid Username/Password. Try again.')
                    self.client.close()

            elif 'LIST' in comm:
                c=0
                user= Line_1.split('|||')[1]
                password= Line_1.split('|||')[2]
                folder= Line_1.split('|||')[3]
                try:
                    with open ('dfs.conf','r') as fh:
                        conf=fh.read().split()
                except:
                    conf=['admin','admin123']
                Auth= False
                for i in range (len(conf)):
                    if user==conf[i] and password==conf[i+1]:
                        Auth=True
                        try:
                            dirs = os.listdir(minfolder+'/'+folder)
                            self.client.send(b'200 ready ')
                            Message=b''
                            while c < len(dirs):
                                Message+= dirs[c].encode() +b' '
                                c += 1
                            print(Message)
                            os.system('clear')
                            print('The HTTP Server is running on port {port} ...'.format(port=self.PORT))
                            self.client.send(Message)
                            self.client.close()

                        except:
                            self.client.send(b'500 folder does not exisit')
                            self.client.close()
                    i+=2

                if not Auth:
                    self.client.send(b'400 Invalid Username/Password. Try again.')
                    self.client.close()
                
                

        except:
            self.client.close()
            pass

    def Generator(self,minfolder):
        # generate new socket
        self.listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen.bind(self.SERVER_ADDRESS)
        self.listen.listen(self.REQUEST_QUEUE_SIZE)
        print('The HTTP Server is running on port {port} ...'.format(port=self.PORT))
        # x = time.time() + 60
        # download_thread = threading.Thread(target=self.reset(x), args=x)
        # download_thread.start()

        while True:
            # Signal (Set handlers for asynchronous events)
            # Signal.signal(signalnum, handler): Set the handler for signal signalnum to the function handler.
            # SIGCHLD event to hand multi request.
            # Reference: https://docs.python.org/2/library/signal.html
            signal.signal(signal.SIGCHLD, self.DeadPool)
            # Accept Request
            try:
                self.client, self.client_address = self.listen.accept()

            except IOError as e:
                code, msg = e.args
                # restart the connection if there was interrupted
                # Erron.EINTER "Interrupted system call"
                # Reference: https://docs.python.org/2/library/errno.html
                if code == errno.EINTR:
                    continue
                else:
                    raise
                pass
                # Create Process IDentifier
            pid = os.fork()
            if pid == 0:  # check of it is new request
                self.listen.close()  # close the listen request
                self.WorkStation(minfolder)  # handle the client request

                os._exit(0)
            else:  # parent
                self.client.close()  # close the request


if __name__ == '__main__':
    server = Server()
