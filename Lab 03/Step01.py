#!/usr/bin/env python3
import socket

#the code provide in the beginning of the assignment
CRFL = "\r\n"

def calibrate(): 
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((target_host, target_port))
  firstline = "GET /hello HTTP/1.1" + CRFL
  request = CRFL + firstline
  client.send(request.encode())
  httpresponse = client.recv(8192)
  response = httpresponse.decode()
  httpresponse = client.recv(8192)
  response = response + httpresponse
  client.close()
  print(response)

if __name__ == "__main__":
  calibrate()
