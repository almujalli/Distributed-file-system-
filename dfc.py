# !/usr/bin/env python3

import socket
import os
import time
import hashlib

while True:
    try:
        with open('dfc.conf','r') as fh:
            conf=fh.read().split() 
        web= conf[2]
        port1=int(conf[3])
        port2=int(conf[7])
        port3=int(conf[11])
        port4=int(conf[15])
        user= conf[17]
        password= conf[19]
    except:
        print('Something wrong')

    command=input('Client command: ')
    menu=0
    ftest=''
    if len(command.split(' ')) >= 2:
        if 'PUT' in command.split(' ')[0]:
            if os.path.isfile(command.split(' ')[1]): 
                menu=1
                ftest= command.split(' ')[1]
                try:
                    if command.split(' ')[2]:
                        supfolder=command.split(' ')[2]
                        if not '/' in supfolder:
                            supfolder= '/'+ supfolder
                    else:
                        
                        supfolder='/home'
                except:
                    supfolder='/home'
            else:
                print('file is not there')
        elif 'GET' in command.split(' ')[0]:
            menu=2
            ftest=command.split(' ')[1]
            try:
                if command.split(' ')[2]:
                    supfolder=command.split(' ')[2]
                    if not '/' in supfolder:
                        supfolder= '/'+ supfolder
                else:
                    supfolder='/home'
            except:
                supfolder='/home'

        elif 'LIST' in command.split(' ')[0]:
            menu=3
            try:
                if command.split(' ')[1]:
                    supfolder=command.split(' ')[1]
                    AllFolder= False 
                    if not '/' in supfolder:
                        supfolder= '/'+ supfolder
                else:
                    AllFolder=True
                    supfolder='/home'
            except:
                AllFolder=True
                supfolder='/home'
        else:
            print("commmand unknown try agin")
    else:
        print("erro command try again")
    
    if menu ==1:
        if len(str(os.path.getsize(ftest)/4).split('.')) >1 :
            if int(str(os.path.getsize(ftest)/4).split('.')[1]) == 25:
                P1size=int(str(os.path.getsize(ftest)/4).split('.')[0]) +1
                P2size=int(str(os.path.getsize(ftest)/4).split('.')[0])
                P3size=int(str(os.path.getsize(ftest)/4).split('.')[0])
                P4size=int(str(os.path.getsize(ftest)/4).split('.')[0])
            elif int(str(os.path.getsize(ftest)/4).split('.')[1]) == 50:
                P1size=int(str(os.path.getsize(ftest)/4).split('.')[0]) +1
                P2size=int(str(os.path.getsize(ftest)/4).split('.')[0]) +1
                P3size=int(str(os.path.getsize(ftest)/4).split('.')[0])
                P4size=int(str(os.path.getsize(ftest)/4).split('.')[0])

            elif int(str(os.path.getsize(ftest) / 4).split('.')[1]) == 75:
                P1size=int(str(os.path.getsize(ftest)/4).split('.')[0]) +1
                P2size=int(str(os.path.getsize(ftest)/4).split('.')[0]) +1
                P3size=int(str(os.path.getsize(ftest)/4).split('.')[0]) +1
                P4size=int(str(os.path.getsize(ftest)/4).split('.')[0])
            else:
                P1size = int(str(os.path.getsize(ftest) / 4).split('.')[0])
                P2size = int(str(os.path.getsize(ftest) / 4).split('.')[0])
                P3size = int(str(os.path.getsize(ftest) / 4).split('.')[0])
                P4size = int(str(os.path.getsize(ftest) / 4).split('.')[0])
        else:
            print("Error")
        HashFileRecived = hashlib.md5()
        with open(ftest, 'rb') as fh:
            buf = fh.read()
            HashFileRecived.update(buf)
        planx=int(HashFileRecived.hexdigest(),16)%4
# |-----------------------------------------|
# | X value | DFS1  | DFS2  | DFS3  | DFS4  |
# |     0   | (1,2) | (2,3) | (3,4) | (4,1) |
# |     1   | (4,1) | (1,2) | (2,3) | (3,4) |
# |     2   | (3,4) | (4,1) | (1,2) | (2,3) |
# |     3   | (2,3) | (3,4) | (4,1) | (1,2) |
# |-----------------------------------------|

        with open (ftest, 'rb') as fh:
            P1 = fh.read(P1size)
            P2 = fh.read(P2size)
            P3 = fh.read(P3size)
            P4 = fh.read(P4size)
        
        # |--------------------------------------------X=0------------------------------------------------------------------|
        comm10=b'PUT|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm20=b'PUT|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm30=b'PUT|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm40=b'PUT|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        # |--------------------------------------------X=0------------------------------------------------------------------|
        comm11=b'PUT|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm21=b'PUT|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm31=b'PUT|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm41=b'PUT|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        # |--------------------------------------------X=0------------------------------------------------------------------|
        comm12=b'PUT|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm22=b'PUT|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm32=b'PUT|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm42=b'PUT|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        # |--------------------------------------------X=0------------------------------------------------------------------|
        comm13=b'PUT|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm23=b'PUT|||'+ftest.encode()+b'.P3|||'+str(P3size).encode()+b'|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm33=b'PUT|||'+ftest.encode()+b'.P4|||'+str(P4size).encode()+b'|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm43=b'PUT|||'+ftest.encode()+b'.P1|||'+str(P1size).encode()+b'|||'+ftest.encode()+b'.P2|||'+str(P2size).encode()+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()

        #------------------------------------------- PUT file --------------------------------------------------------------#
        # |--------------------------------------------X=0------------------------------------------------------------------|
        if planx==0:
            # Server 1 ready to test
            try: 
                DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS1.connect((web, port1))
                DFS1.send(comm10)
                DFS1.settimeout(1.0)
                d1 = DFS1.recv(1024)
                DFS1.settimeout(None)
                Line_1 = d1.decode()
                if d1.decode().split(' ')[0]=='200':
                    DFS1.send(P1)
                    d1=DFS1.recv(1024)
                    if d1.decode().split(' ')[0]=='200':
                        DFS1.send(P2)
                else:
                    print(Line_1)
            except:
                pass
            # Server 2 ready to test 
            try: 
                DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS2.connect((web, port2))
                DFS2.send(comm20)
                DFS2.settimeout(1.0)
                d2 = DFS2.recv(1024)
                DFS2.settimeout(None)
                Line_2 = d2.decode()
                if d2.decode().split(' ')[0]=='200':
                    DFS2.send(P2)
                    d2=DFS2.recv(1024)
                    if d2.decode().split(' ')[0]=='200':
                        DFS2.send(P3)
                else:
                    print(Line_2)
            except:
                pass
            # Server 3 ready to test
            try: 
                DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS3.connect((web, port3))
                DFS3.send(comm30)
                DFS3.settimeout(1.0)
                d3 = DFS3.recv(1024)
                DFS3.settimeout(None)
                Line_3 = d3.decode()
                if d3.decode().split(' ')[0]=='200':
                    DFS3.send(P3)
                    d3=DFS3.recv(1024)
                    if d3.decode().split(' ')[0]=='200':
                        DFS3.send(P4)
                else:
                    print(Line_3)
            except:
                pass
                
            # Server 4 ready 
            try: 
                DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS4.connect((web, port4))
                DFS4.send(comm40)
                DFS4.settimeout(1.0)
                d4 = DFS4.recv(1024)
                DFS4.settimeout(None)
                Line_4 = d4.decode()
                if d4.decode().split(' ')[0]=='200':
                    DFS4.send(P4)
                    d4=DFS4.recv(1024)
                    if d4.decode().split(' ')[0]=='200':
                        DFS4.send(P1)
                else:
                    print(Line_4)
            except:
                pass
        # |--------------------------------------------X=1------------------------------------------------------------------|
        elif planx==1:
            # Server 1 ready to test
            try: 
                DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS1.connect((web, port1))
                DFS1.send(comm11)
                DFS1.settimeout(1.0)
                d1 = DFS1.recv(1024)
                DFS1.settimeout(None)
                Line_1 = d1.decode()
                if d1.decode().split(' ')[0]=='200':
                    DFS1.send(P4)
                    d1=DFS1.recv(1024)
                    if d1.decode().split(' ')[0]=='200':
                        DFS1.send(P1)
                else:
                    print(Line_1)
            except:
                pass
            # Server 2 ready to test 
            try: 
                DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS2.connect((web, port2))
                DFS2.send(comm21)
                DFS2.settimeout(1.0)
                d2 = DFS2.recv(1024)
                DFS2.settimeout(None)
                Line_2 = d2.decode()
                if d2.decode().split(' ')[0]=='200':
                    DFS2.send(P1)
                    d2=DFS2.recv(1024)
                    if d2.decode().split(' ')[0]=='200':
                        DFS2.send(P2)
                else:
                    print(Line_2)
            except:
                pass
            # Server 3 ready to test
            try: 
                DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS3.connect((web, port3))
                DFS3.send(comm31)
                DFS3.settimeout(1.0)
                d3 = DFS3.recv(1024)
                DFS3.settimeout(None)
                Line_3 = d3.decode()
                if d3.decode().split(' ')[0]=='200':
                    DFS3.send(P2)
                    d3=DFS3.recv(1024)
                    if d3.decode().split(' ')[0]=='200':
                        DFS3.send(P3)
                else:
                    print(Line_3)
            except:
                pass
                
            # Server 4 ready 
            try: 
                DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS4.connect((web, port4))
                DFS4.send(comm41)
                DFS4.settimeout(1.0)
                d4 = DFS4.recv(1024)
                DFS4.settimeout(None)
                Line_4 = d4.decode()
                if d4.decode().split(' ')[0]=='200':
                    DFS4.send(P3)
                    d4=DFS4.recv(1024)
                    if d4.decode().split(' ')[0]=='200':
                        DFS4.send(P4)
                else:
                    print(Line_4)
            except:
                pass
        elif planx==2:
            # Server 1 ready to test
            try: 
                DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS1.connect((web, port1))
                DFS1.send(comm12)
                DFS1.settimeout(1.0)
                d1 = DFS1.recv(1024)
                DFS1.settimeout(None)
                Line_1 = d1.decode()
                if d1.decode().split(' ')[0]=='200':
                    DFS1.send(P3)
                    d1=DFS1.recv(1024)
                    if d1.decode().split(' ')[0]=='200':
                        DFS1.send(P4)
                else:
                    print(Line_1)
            except:
                pass
            # Server 2 ready to test 
            try: 
                DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS2.connect((web, port2))
                DFS2.send(comm22)
                DFS2.settimeout(1.0)
                d2 = DFS2.recv(1024)
                DFS2.settimeout(None)
                Line_2 = d2.decode()
                if d2.decode().split(' ')[0]=='200':
                    DFS2.send(P4)
                    d2=DFS2.recv(1024)
                    if d2.decode().split(' ')[0]=='200':
                        DFS2.send(P1)
                else:
                    print(Line_2)
            except:
                pass
            # Server 3 ready to test
            try: 
                DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS3.connect((web, port3))
                DFS3.send(comm32)
                DFS3.settimeout(1.0)
                d3 = DFS3.recv(1024)
                DFS3.settimeout(None)
                Line_3 = d3.decode()
                if d3.decode().split(' ')[0]=='200':
                    DFS3.send(P1)
                    d3=DFS3.recv(1024)
                    if d3.decode().split(' ')[0]=='200':
                        DFS3.send(P2)
                else:
                    print(Line_3)
            except:
                pass
                
            # Server 4 ready to test p2 p3 
            try: 
                DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS4.connect((web, port4))
                DFS4.send(comm42)
                DFS4.settimeout(1.0)
                d4 = DFS4.recv(1024)
                DFS4.settimeout(None)
                Line_4 = d4.decode()
                if d4.decode().split(' ')[0]=='200':
                    DFS4.send(P2)
                    d4=DFS4.recv(1024)
                    if d4.decode().split(' ')[0]=='200':
                        DFS4.send(P3)
                else:
                    print(Line_4)
            except:
                pass
        elif planx==3:
            # Server 1 ready to test
            try: 
                DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS1.connect((web, port1))
                DFS1.send(comm13)
                DFS1.settimeout(1.0)
                d1 = DFS1.recv(1024)
                DFS1.settimeout(None)
                Line_1 = d1.decode()
                if d1.decode().split(' ')[0]=='200':
                    DFS1.send(P2)
                    d1=DFS1.recv(1024)
                    if d1.decode().split(' ')[0]=='200':
                        DFS1.send(P3)
                else:
                    print(Line_1)
            except:
                pass
            # Server 2 ready to test 
            try: 
                DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS2.connect((web, port2))
                DFS2.send(comm23)
                DFS2.settimeout(1.0)
                d2 = DFS2.recv(1024)
                DFS2.settimeout(None)
                Line_2 = d2.decode()
                if d2.decode().split(' ')[0]=='200':
                    DFS2.send(P3)
                    d2=DFS2.recv(1024)
                    if d2.decode().split(' ')[0]=='200':
                        DFS2.send(P4)
                else:
                    print(Line_2)
            except:
                pass
            # Server 3 ready to test
            try: 
                DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS3.connect((web, port3))
                DFS3.send(comm33)
                DFS3.settimeout(1.0)
                d3 = DFS3.recv(1024)
                DFS3.settimeout(None)
                Line_3 = d3.decode()
                if d3.decode().split(' ')[0]=='200':
                    DFS3.send(P4)
                    d3=DFS3.recv(1024)
                    if d3.decode().split(' ')[0]=='200':
                        DFS3.send(P1)
                else:
                    print(Line_3)
            except:
                pass
                
            # Server 4 ready to test p2 p3 
            try: 
                DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS4.connect((web, port4))
                DFS4.send(comm43)
                DFS4.settimeout(1.0)
                d4 = DFS4.recv(1024)
                DFS4.settimeout(None)
                Line_4 = d4.decode()
                if d4.decode().split(' ')[0]=='200':
                    DFS4.send(P1)
                    d4=DFS4.recv(1024)
                    if d4.decode().split(' ')[0]=='200':
                        DFS4.send(P2)
                else:
                    print(Line_4)
            except:
                pass
        else:
            print("Error")
        DFS1.close()
        DFS2.close()
        DFS3.close()
        DFS4.close()

    elif menu==2:
        comm = b'GET|||'+ftest.encode() +b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm1 = b'FIND|||'+ftest.encode() +b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()

        try:
            os.mkdir('DFC/')
        except:
            pass
        try:
            os.mkdir('DFC/'+user)
        except:
            pass
        

        try:
            L1=[]
            DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DFS1.connect((web, port1))
            DFS1.send(comm1)
            DFS1.settimeout(1.0)
            data1 = DFS1.recv(1024)
            DFS1.settimeout(None)
            Line_1 = data1.decode()
            if data1.decode().split('|||')[0]=='200':
                for i in range (len(data1.decode().split('|||'))):
                    if i != 0 and i != len(data1.decode().split('|||'))-1:
                        L1.append('DFS1|||'+data1.decode().split('|||')[i])
            else: 
                print(Line_1)
        except:
            pass


        try:
            L2=[]
            DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DFS2.connect((web, port2))
            DFS2.send(comm1)
            DFS2.settimeout(1.0)
            data2 = DFS2.recv(1024)
            DFS2.settimeout(None)
            Line_2 = data2.decode()
            if data2.decode().split('|||')[0]=='200':
                for i in range (len(data2.decode().split('|||'))):
                    if i != 0 and i != len(data2.decode().split('|||'))-1:
                        L2.append('DFS2|||'+data2.decode().split('|||')[i])
            else: 
                print(Line_2)
        except:
            pass

        try:
            L3=[]
            DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DFS3.connect((web, port3))
            DFS3.send(comm1)
            DFS3.settimeout(1.0)
            data3 = DFS3.recv(1024)
            DFS3.settimeout(None)
            Line_3 = data3.decode()
            if data3.decode().split('|||')[0]=='200':
                for i in range (len(data3.decode().split('|||'))):
                    if i != 0 and i != len(data3.decode().split('|||'))-1:
                        L3.append('DFS3|||'+data3.decode().split('|||')[i])
            else: 
                print(Line_3)
        except:
            pass

        try:
            L4=[]
            DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DFS4.connect((web, port4))
            DFS4.send(comm1)
            DFS4.settimeout(1.0)
            data4 = DFS4.recv(1024)
            DFS4.settimeout(None)
            Line_4 = data4.decode()
            if data4.decode().split('|||')[0]=='200':
                for i in range (len(data4.decode().split('|||'))):
                    if i != 0 and i != len(data4.decode().split('|||'))-1:
                        L4.append('DFS4|||'+data4.decode().split('|||')[i])
            else: 
                print(Line_4)
        except:
            pass

        L=[]
        L=L1+L2+L3+L4
        ccx=0

        if len(L)>=4:
            for i in range (len(L)):
                server=L[i].split('|||')[0]
                file = L[i].split('|||')[1]
                if not os.path.isfile('DFC/'+user+'/'+file):
                    ccx+=1 
                    comm = b'GET|||'+file.encode() +b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
                    if server=='DFS1':
                        try:
                            DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            DFS1.connect((web, port1))
                            DFS1.send(comm)
                            DFS1.settimeout(1.0)
                            data1 = DFS1.recv(1024)
                            DFS1.settimeout(None)
                            Line_1 = data1.decode()
                            if data1.decode().split('|||')[0]=='200':
                                filesize=int(data1.decode().split('|||')[1])
                                fh= open('DFC/'+user+'/'+file, 'wb')
                                DFS1.send(b'200 ready_to_receive')
                                c=0
                                while c<filesize:
                                    # receive data from web server
                                    data1 = DFS1.recv(1024)
                                    if (len(data1) > 0):
                                        c+=1024
                                # send to browser
                                # self.client.send(data)
                                # http_response += data
                                        fh.write(data1)
                                    else:
                                        break
                                fh.close()

                            else: 
                                print(Line_1)
                        except:
                            pass

                    elif server=='DFS2':
                        try:
                            DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            DFS2.connect((web, port2))
                            DFS2.send(comm)
                            DFS2.settimeout(1.0)
                            data2 = DFS2.recv(1024)
                            DFS2.settimeout(None)
                            Line_2 = data2.decode()
                            if data2.decode().split('|||')[0]=='200':
                                filesize=int(data2.decode().split('|||')[1])
                                fh= open('DFC/'+user+'/'+file, 'wb')
                                DFS2.send(b'200 ready_to_receive')
                                c=0
                                while c<filesize:
                                # receive data from web server
                                    data2 = DFS2.recv(1024)
                                    if (len(data2) > 0):
                                        c+=1024
                                # send to browser
                                # self.client.send(data)
                                # http_response += data
                                        fh.write(data2)
                                    else:
                                        break
                                fh.close()

                            else: 
                                print(Line_2)
                        except:
                            pass


                    elif server=='DFS3':
                        try:
                            DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            DFS3.connect((web, port3))
                            DFS3.send(comm)
                            DFS3.settimeout(1.0)
                            data3 = DFS3.recv(1024)
                            DFS3.settimeout(None)
                            Line_3 = data3.decode()
                            if data3.decode().split('|||')[0]=='200':
                                filesize=int(data3.decode().split('|||')[1])
                                fh= open('DFC/'+user+'/'+file, 'wb')
                                DFS3.send(b'200 ready_to_receive')
                                c=0
                                while c<filesize:
                                # receive data from web server
                                    data3 = DFS3.recv(1024)
                                    if (len(data3) > 0):
                                        c+=1024
                                # send to browser
                                # self.client.send(data)
                                # http_response += data
                                        fh.write(data3)
                                    else:
                                        break
                                fh.close()

                            else: 
                                print(Line_3)
                        except:
                            pass

                    elif server=='DFS4':
                        try:
                            DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            DFS4.connect((web, port4))
                            DFS4.send(comm)
                            DFS4.settimeout(1.0)
                            data4 = DFS4.recv(1024)
                            DFS4.settimeout(None)
                            Line_4 = data4.decode()
                            if data4.decode().split('|||')[0]=='200':
                                filesize=int(data4.decode().split('|||')[1])
                                fh= open('DFC/'+user+'/'+file, 'wb')
                                DFS4.send(b'200 ready_to_receive')
                                c=0
                                while c<filesize:
                                # receive data from web server
                                    data4 = DFS4.recv(1024)
                                    if (len(data4) > 0):
                                        c+=1024
                                # send to browser
                                # self.client.send(data)
                                # http_response += data
                                        fh.write(data4)
                                    else:
                                        break
                                fh.close()

                            else: 
                                print(Line_4)
                        except:
                            pass






            fh3=open('DFC/'+user+'/'+ftest,'wb')
            c=0
            for root, dirs, files in os.walk('DFC/'+user+'/'):
                for i in range(5):
                    if ftest+ '.P' + str(i) in files:
                        with open ('DFC/'+user+'/'+ftest+ '.P' + str(i), 'rb') as fh:
                            fh3.write(fh.read())
                        os.remove("DFC/"+user+'/'+ftest+ '.P' + str(i))
                        c+=1

            fh3.close()
            if c==4:
                print('download is complete')
            else:
                print('Erorr file missing part')
                os.remove("DFC/"+user+'/'+ftest)
        else:
            print('Erorr file missing part')


    elif menu==3:
        if AllFolder:
            supfolder='/'

        comm1 = b'ROOT|||'+ftest.encode() +b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        comm = b'LIST'+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
        try:
            L=[]
            DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            DFS1.connect((web, port1))
            DFS1.send(comm1)
            DFS1.settimeout(1.0)
            data1 = DFS1.recv(1024)
            DFS1.settimeout(None)
            Line_1 = data1.decode()
            if data1.decode().split('|||')[0]=='200':
                for i in range (len(data1.decode().split('|||'))):
                    if i != 0:
                        L.append(data1.decode().split('|||')[i])
            else: 
                print(Line_1)
        except:
            try:
                L=[]
                DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS2.connect((web, port2))
                DFS2.send(comm1)
                DFS2.settimeout(1.0)
                data2 = DFS2.recv(1024)
                DFS2.settimeout(None)
                Line_2 = data2.decode()
                if data2.decode().split('|||')[0]=='200':
                    for i in range (len(data2.decode().split('|||'))):
                        if i != 0:
                            L.append(data2.decode().split('|||')[i])
                else: 
                    print(Line_2)
            except:
                try:
                    L=[]
                    DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    DFS3.connect((web, port3))
                    DFS3.send(comm1)
                    DFS3.settimeout(1.0)
                    data3 = DFS3.recv(1024)
                    DFS3.settimeout(None)
                    Line_3 = data3.decode()
                    if data3.decode().split('|||')[0]=='200':
                        for i in range (len(data3.decode().split('|||'))):
                            if i != 0:
                                L.append(data3.decode().split('|||')[i])
                    else: 
                        print(Line_3)
                except:
                    try:
                        L=[]
                        DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        DFS4.connect((web, port4))
                        DFS4.send(comm1)
                        DFS4.settimeout(1.0)
                        data4 = DFS4.recv(1024)
                        DFS4.settimeout(None)
                        Line_4 = data4.decode()
                        if data4.decode().split('|||')[0]=='200':
                            for i in range (len(data4.decode().split('|||'))):
                                if i != 0:
                                    L.append(data4.decode().split('|||')[i])
                        else: 
                            print(Line_4)
                    except:
                        L=[]
                        print('erorr')


        for i in range (len(L)):
            print(L[i])
            supfolder=L[i]
            comm = b'LIST'+b'|||'+user.encode()+b'|||'+password.encode()+b'|||'+supfolder.encode()
            x=[]
            try:
                DFS1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS1.connect((web, port1))
                DFS1.send(comm)
                DFS1.settimeout(1.0)
                d1 = DFS1.recv(1024)
                DFS1.settimeout(None)
                if d1.decode().split(' ')[0]=='200':
                    data1 = DFS1.recv(999999)
                    Line_1 = data1.decode().split(' ')
                    FLine_1=[]
                    for i in range (len(Line_1)):
                        if len(Line_1[i].split('.')) >=3:
                            FLine_1.append(Line_1[i])
                    x+=FLine_1
                else:
                    print(d1.decode())
            except:
                pass

            try:
                DFS2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS2.connect((web, port2))
                DFS2.send(comm)
                DFS2.settimeout(1.0)
                d2 = DFS2.recv(1024)
                DFS2.settimeout(None)
                if d2.decode().split(' ')[0]=='200':
                    data2 = DFS2.recv(999999)
                    Line_2 = data2.decode().split(' ')
                    FLine_2=[]
                    for i in range (len(Line_2)):
                        if len(Line_2[i].split('.')) >=3:
                            FLine_2.append(Line_2[i])
                    x+=FLine_2
                else:
                    print(d2.decode())
            except:
                pass

            try:
                DFS3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS3.connect((web, port3))
                DFS3.send(comm)
                DFS3.settimeout(1.0)
                d3 = DFS3.recv(1024)
                DFS3.settimeout(None)
                if d3.decode().split(' ')[0]=='200':
                    data3 = DFS3.recv(999999)
                    Line_3 = data3.decode().split(' ')
                    FLine_3=[]
                    for i in range (len(Line_3)):
                        if len(Line_3[i].split('.')) >=3:
                            FLine_3.append(Line_3[i])
                    x+=FLine_3
                else:
                    print(d3.decode())
            except:
                pass


            try:
                DFS4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                DFS4.connect((web, port4))
                DFS4.send(comm)
                DFS4.settimeout(1.0)
                d4 = DFS4.recv(1024)
                DFS4.settimeout(None)
                if d4.decode().split(' ')[0]=='200':
                    data4 = DFS4.recv(999999)
                    Line_4 = data4.decode().split(' ')
                    FLine_4=[]
                    for i in range (len(Line_4)):
                        if len(Line_4[i].split('.')) >=3:
                            FLine_4.append(Line_4[i])
                    x+=FLine_4
                else:
                    print(d4.decode())
            except:
                pass

            try:
                y=[]
                for i in range (len(x)):
                    if not x[i] in y :
                        y.append(x[i])
                maxa=0
                z=[]
                z1=[]
                for i in range (len(y)):
                    counter=0
                    for c in range(len(y)):
                        if ((y[i].split('.')[0]+'.'+y[i].split('.')[1])==(y[c].split('.')[0]+'.'+y[c].split('.')[1])):
                            if not y[i].split('.')[0]+'.'+y[i].split('.')[1] in z1:
                                z1.append(y[i].split('.')[0]+'.'+y[i].split('.')[1])
                            counter+=1
                            if counter == 4:
                                if not y[i].split('.')[0]+'.'+y[i].split('.')[1] in z:
                                    z.append(y[i].split('.')[0]+'.'+y[i].split('.')[1])
            
                for i in range(len(z1)): 
                    if z1[i] in z: 
                        print(z1[i])
                    else:
                        print(z1[i] + ' [incomplete] ')
            except:
                print('Error list can not be printing')

    try:
        fh1.close()
        fh2.close()
        fh3.close()
    except:
        pass
    




