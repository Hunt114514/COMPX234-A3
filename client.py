import socket
import sys

def send_request(host,port,request):
      client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      client_socket.connect((host,port))
      client_socket.send(request.encode('utf-8'))
      response = client_socket.recv(1024).decode('utf-8')
      client_socket.close()
      return response
    