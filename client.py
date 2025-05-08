import socket
import sys

def send_request(host,port,request):
      client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
      client_socket.connect((host,port))
      client_socket.send(request.encode('utf-8'))
      response = client_socket.recv(1024).decode('utf-8')
      client_socket.close()
      return response

def main():
    if len(sys.argv)!=4:
            print("Usage: python client.py <host> <port> <request_file>")
            sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]

    with open(request_file, 'r') as file:
          for line in line:
                line =line.strip()
                if not line:
                      continue
                parts = line.split()
                command = parts[0]
                key = parts[1]
                value = parts[2] if len(parts) == 3 else ""
                message_size = len(line) + 3
                request = f"{message_size:03d}{command[0]}{key}{value}"
                response = send_request(host,port,request)
                print(f"{line}:{response[3:]}")

if __name__=="_main_":
      main()


    