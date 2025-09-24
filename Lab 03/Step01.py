#!/usr/bin/env python3
import socket

#Using the provided information about the webhost
target_port = 380
target_host = "hw3.csec380.fun"
endpoint = "/hello"

#the code provide in the beginning of the assignment
CRFL = "\r\n"

def calibrate(): 
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((target_host, target_port))

  
  #request generation
  firstline = "GET /hello HTTP/1.1" + CRFL
  request = CRFL + firstline
  client.send(request.encode())
  #response parsing
  httpresponse = client.recv(8192)
  response = httpresponse.decode()

  client.close()
  print(response)

if __name__ == "__main__":
  calibrate()
