#! /usr/bin/env python3

      # for params
import sys, re, socket, os
sys.path.append("../lib") 
import params
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

sock, addr = lsock.accept() # Here it sits to wait for client

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

while True:

    payload = framedReceive(sock, debug)
    print(payload)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    framedSend(sock, payload, debug)

    fileName = payload.decode()
    if os.path.isfile(fileName):
        print(fileName)
        with open("server"+fileName,"wb") as file:
            print("Opening file...")
            while True:
                print("receiving data")
                data = framedReceive(sock, debug)
                if debug: print("rec'd: ", data)
                if not data:
                    print("breaking")
                    break
                framedSend(sock, data, debug)
                print(data)
                file.write(data)

    #payload += b"!"             # make emphatic!
    

