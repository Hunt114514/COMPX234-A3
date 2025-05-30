import socket
import threading
import time

class TupleSpace:
    def _init_(self):
        self.tuples = {}
        self.client_count = 0
        self.operation_count = 0
        self.read_count = 0
        self.get_count = 0
        self.put_count = 0
        self.error_count = 0

    def put(self,key,value):
        if key in self.tuples:
            self.error_count +=1
            return 1
        self.tuples[key] = value
        self.put_count +=1
        return 0
    
    def read(self, key):
        if key in self.tuples:
            self.read_count += 1
            return self.tuples[key]
        self.error_count += 1
        return ""
    
    def get(self, key):
        if key in self.tuples:
            value = self.tuples.pop(key)
            self.get_count += 1
            return value
        self.error_count += 1
        return ""

    def get_summary(self):
        tuple_count = len(self.tuples)
        if tuple_count == 0:
            avg_tuple_size = 0
            avg_key_size = 0
            avg_value_size = 0
        else:
            total_tuple_size = sum(len(key) + len(value) for key, value in self.tuples.items())
            total_key_size = sum(len(key) for key in self.tuples.keys())
            total_value_size = sum(len(value) for value in self.tuples.values())
            avg_tuple_size = total_tuple_size / tuple_count
            avg_key_size = total_key_size / tuple_count
            avg_value_size = total_value_size / tuple_count
        return {
            "tuple_count": tuple_count,
            "avg_tuple_size": avg_tuple_size,
            "avg_key_size": avg_key_size,
            "avg_value_size": avg_value_size,
            "client_count": self.client_count,
            "operation_count": self.operation_count,
            "read_count": self.read_count,
            "get_count": self.get_count,
            "put_count": self.put_count,
            "error_count": self.error_count
        }
    
def handle_client(client_socket,tuple_space):
    tuple_space.client_count += 1
    while True:
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                break
            message_size = int(request[:3])
            command = request[3]
            key = request[4:message_size - 1].strip()
            value = request[message_size - 1:].strip() if command == 'P' else ""

            if command == 'R':
                result = tuple_space.read(key)
                if result:
                    response = f"{len(f'OK ({key}, {result}) read'):03d} OK ({key}, {result}) read"
                else:
                    response = f"{len(f'ERR {key} does not exist'):03d} ERR {key} does not exist"
            elif command == 'G':
                result = tuple_space.get(key)
                if result:
                    response = f"{len(f'OK ({key}, {result}) removed'):03d} OK ({key}, {result}) removed"
                else:
                    response = f"{len(f'ERR {key} does not exist'):03d} ERR {key} does not exist"
            elif command == 'P':
                result = tuple_space.put(key, value)
                if result == 0:
                    response = f"{len(f'OK ({key}, {value}) added'):03d} OK ({key}, {value}) added"
                else:
                    response = f"{len(f'ERR {key} already exists'):03d} ERR {key} already exists"
            else:
                response = f"{len('ERR invalid command'):03d} ERR invalid command"

            tuple_space.operation_count += 1
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()

def main():
    port = 51234
    tuple_space = TupleSpace()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    def print_summary():
        while True:
            time.sleep(10)
            summary = tuple_space.get_summary()
            print(f"Tuple space summary:")
            print(f"Number of tuples: {summary['tuple_count']}")
            print(f"Average tuple size: {summary['avg_tuple_size']}")
            print(f"Average key size: {summary['avg_key_size']}")
            print(f"Average value size: {summary['avg_value_size']}")
            print(f"Total clients connected: {summary['client_count']}")
            print(f"Total operations: {summary['operation_count']}")
            print(f"Total READs: {summary['read_count']}")
            print(f"Total GETs: {summary['get_count']}")
            print(f"Total PUTs: {summary['put_count']}")
            print(f"Total errors: {summary['error_count']}")
            print("-" * 50)

    summary_thread = threading.Thread(target=print_summary)
    summary_thread.daemon = True
    summary_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, tuple_space))
        client_thread.start()

if __name__ == "__main__":
    main()
