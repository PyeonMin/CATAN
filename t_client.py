import socket
import threading
from innersetting import *


class Server:
    def __init__(self, host):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(host)

    def send(self, value):
        self.socket.send(f"{value}".encode())

    def recv(self):
        return self.socket.recv(1024)


class TradeClient:
    def __init__(self, host: tuple) -> None:
        self.server = Server(host)
        
        self.name = "noname"
        self.resource = [0,0,0,0,0]
        
        receiver_thread = threading.Thread(target=self.recv_data)
        receiver_thread.start()
           
    def set_name(self):
        while 1:
            name = input('사용할 이름을 입력하세요:')
            self.server.send(name)
            
            data = self.server.recv().decode()
            if data == State.Available:
                self.name = name
                break
         
    def recv_data(self):
        self.log("receiving")
        while 1:
            data = self.server.recv().decode().split(" ")
            command, value =  data[0], data[1:]
            
            self.log(data)  
            if command == Commands.SET_NAME:
                self.set_name()
            
            elif command == Commands.DEAL:
                pass
            
            elif command == Commands.SET_RESOURCE:
                self.set_status(value)
                self.log(f"{self.resource}")

            elif command == Commands.TURN:
                self.get_turn()

    def get_turn(self):
        print("내턴임")
        value = input(":")
        self.server.send(value)

    def set_status(self, data):
        print(data)
        for i in range(0, len(Item)):
            self.resource[i] = int(data[i])

    def log(self,msg):
        print(f"client log: {msg}")
            
        
ip = 'localhost'
port = 25565

tclient = TradeClient((ip,port))