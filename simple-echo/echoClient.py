#! /usr/bin/env python3

# Echo client program
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
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

outMessage = "Hello world!"

while len(outMessage):
    print("sending '%s'" % outMessage)
    outMessage = parser(outMessage)
    bytesSent = s.send(outMessage.encode())
    outMessage = outMessage[bytesSent:]

#data = s.recv(1024).decode()
#print("Received '%s'" % data)

outMessage = "Hello world!"
while len(outMessage):
    print("sending '%s'" % outMessage)
    outMessage = parser(outMessage)
    bytesSent = s.send(outMessage.encode())
    outMessage = outMessage[bytesSent:]

s.shutdown(socket.SHUT_WR)      # no more output
data = ""
while 1:
	while isIncomplete(data):
		data = data+s.recv(1024).decode()
		if len(data) == 0:
			break
	if len(data) == 0:
		print("Zero length read, nothing to send, terminating")
		break
	dataArray = dataParser(data)
	data = dataArray[0]
	print("Received '%s'" % data)
	if len(data) == 0:
		break
	data = dataArray[1]
print("Zero length read.  Closing")
s.close()
