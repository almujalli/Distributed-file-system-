
# Distributed file system  


A distributed file system handels the multithreading request using an operation system (Fork) from multi-clients written with python 3.6.3. The program has two files a dfc.py and a dfs.py which use to get a file, put a file and list files. The dfs.py uses to creat four distributed servers (10001 - 10004) to handl three functions which are (PUT: to upload a file, GET: to download a file and LIST: to show the files in the DFS)  


# Date and Version
2017.03.12

1.5.7


# How it works
PUT Function (Upload a file to DFS) 

* The user enters the command in the terminal (<a style='color:green'> PUT 1.txt or PUT 1.txt /Download</a>) 
* The program  accepts the request, anlyizets to make sure it valued and checks if the file there.
* The program splits the file in to 4 equal length pieces P1, P2, P3, P4 using hashing function and % 4.
* Depends on the result, The program sends two pieces to different servers (10001-10004)
 
	  value | DFS1  | DFS2  | DFS3  | DFS4 
	  0     | (1,2) | (2,3) | (3,4) | (4,1) 
	  1     | (4,1) | (1,2) | (2,3) | (3,4) 
	  2     | (3,4) | (4,1) | (1,2) | (2,3) 
	  3     | (2,3) | (3,4) | (4,1) | (1,2)
      
      # Client command: PUT 1.txt
      # Client command: PUT 1.txt /hi 


GET Function (Download a file from DFS)

* The user enters the command in the terminal (<a style='color:blue'> GET 1.txt or GET 1.txt /Download</a>) 
* The program  accepts the request and anlyizets to make sure it valued.
* The program sends the request to the servers (10001-10004) to check if the file there and if the user is authorized.
* The servers send pices of the file that they have and the client decides which pice should be downlowad.
* The program collects the pieces together in one file.
perfection. 
```javascript
# Client command: GET 1.txt
Download is complete
# Client command: GET 1.txt
Erorr file missing part
# Client command: GET 2.txt
File does not exist
```

LIST Function (List files from DFS)

* The user enters the command in the terminal (<a style='color:red'> LIST or LIST /Download</a>) 
* The program  accepts the request and anlyizets to make sure it valued.
* The program sends the request to the servers (10001-10004) to check if the file there and if the user is authorized.
* The servers send pices of files that they have and the client collects them to make sure if the file is complete or incomplete.
* The program prints the files with their folder.

```javascript
# Client command: LIST 
Bob/
Bob/home
2.pdf
4.docx [incomplete]
3.jpg
1.txt
Bob/hi
1.txt
Bob/hello
2.pdf
# Client command: LIST /hi 
Bob/hi
1.txt
# Client command: LIST /test

```

    

<p align="center">
  <img src="https://www.watchuktvabroad.net/wp-content/uploads/2014/05/cog-icon.png">
</p>

 # Setup
 * Make sure that (socket, os, signal, errno, time, sys,and hashlib) libraries are installed.

# Classes and Functions

There only one classe <a style='color:green'>server</a> and six functions which are <a style='color:red'>init(), Generator(), WorkStation(), DeadPool() and Perfection()</a> 
```javascript
def '__init()__()':
	# Get the folder and the port number from the user and set up the DFS server 
def 'Generation()':
	# wait for a request and generat (Multi-threding) pass it to workstation
def 'WorkStation()':
	# handle the request (PUT/GET/LIST) and pass it to client
def 'deadpool()':
	# close the connection after it has been handel
```


# Used

* To run the code, use this comand in the terminal.

```javascript
DFS servers 

# python3 dfs.py /DFS1 10001 
# python3 dfs.py /DFS2 10002
# python3 dfs.py /DFS3 10003
# python3 dfs.py /DFS4 10004
DFS client

# python3 dfc.py
```
* Make sure that the dfs.conf and dfc.conf are in the same folder 

```javascript
DFC configuration

Server DFS1 127.0.0.1 10001
Server DFS2 127.0.0.1 10002
Server DFS3 127.0.0.1 10003
Server DFS4 127.0.0.1 10004
Username: Bob Password: ComplexPassword

DFS configuration

Alice SimplePassword 
Bob ComplexPassword
```


