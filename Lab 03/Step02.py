#!/usr/bin/env python3
import socket
import time
import json #going to use to alter the headers of requests

#Using the provided information about the webhost
target_port = 380
target_host = "hw3.csec380.fun"
endpoint = "/test"

#the code provide in the beginning of the assignment
CRFL = "\r\n"

def calibrate(): 
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect((target_host, target_port))

  """Changes to make to the code:
    - The header on the user side: must contain 'CSEC-380'
  """

  #request generation
  request = ("GET / HTTP/1.1\r\n"
             "User-Agent: CSEC-380\r\n")
  
  client.sendall(request.encode())
  #response parsing
  httpresponse = client.recv(8192)
  response = httpresponse.decode()
  print(f"Encoded Response: {httpresponse}")
  client.close()
  print(f"Decoded Response: {response}")

if __name__ == "__main__":
  calibrate()