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
