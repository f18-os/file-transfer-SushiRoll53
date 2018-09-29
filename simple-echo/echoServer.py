#! /usr/bin/env python3

# Echo server program

import socket, sys, re
sys.path.append("../lib")       # for params
import params

def parser(message):
    return "@"+message+"$"

def isIncomplete(message):
    startingIndex = message.find("@")
    endingIndex = message.find("$")
    dataArray = []
    if startingIndex == -1 or endingIndex == -1:
        return True
    else:
        return False

def dataParser(message):
    startingIndex = message.find("@")
    endingIndex = message.find("$")
    dataArray = []
    if startingIndex == -1 or endingIndex == -1:
        return dataArray
    else:
        dataArray.append(message[startingIndex+1:endingIndex])
        dataArray.append(message[endingIndex+1:])
        return dataArray 

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )



progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #new stream socket
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)
data = ""
while 1:
	while isIncomplete(data):
		data = data+conn.recv(1024).decode()
		#print("DATA: %s" % data)
		if len(data) == 0:
			break

	if len(data) == 0:
		print("Zero length read, nothing to send, terminating")
		break
	datArray = dataParser(data)
	data = datArray[0]
	sendMsg = "Echoing %s" % data
	print("Received '%s', sending '%s'" % (data, sendMsg))
	sendMsg = parser(sendMsg)
	while len(sendMsg):
		bytesSent = conn.send(sendMsg.encode())
		sendMsg = sendMsg[bytesSent:0]
	data = datArray[1]
conn.shutdown(socket.SHUT_WR)
conn.close()

