import random
import socket
import threading

from innersetting import *

user = 0


class Client:
    @classmethod
    def getClientByAccepted(cls, accepted: tuple):
        socket = accepted[0]
        ip, port = accepted[1]
        return cls(socket, ip, port)

    def __init__(self, socket: socket.socket, ip: str, port: int):
        self.socket = socket
        self.ip = ip
        self.port = port

        self.name = "no_name"
        self.resource = [0, 0, 0, 0, 0]

        self.is_turn = False

    def setRandomResource(self):
        self.resource = [random.randint(0, 5) for _ in range(5)]

    def send(self, value):
        self.socket.send(f"{value}".encode())

    def sendCommand(self, command: Commands, value: str = ""):
        self.socket.send(f"{command} {value}".encode())

    def sendInfo(self):
        self.sendCommand(Commands.SET_RESOURCE, " ".join(map(str, self.resource)))

    def recv(self):
        return self.socket.recv(1024)


class TradingServer:
    people_limit = 3

    def __init__(self, host: tuple):
        self.user = 0

        self.clients = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(host)
        self.server.listen()
        self.log("listening")

    def check(self):
        recent_value = 0
        while 1:
            if recent_value != len(self.clients):
                recent_value = len(self.clients)
                self.log(f"접속자 수:{recent_value}")

    def start(self):
        self.log("server start")
        threading.Thread(target=self.check).start()

        while self.user < 3:
            client = Client.getClientByAccepted(self.server.accept())
            self.user += 1
            self.log(f"{client.port} 처리중")

            threading.Thread(target=self.client_process, args=(client,)).start()

        while self.user != len(self.clients):
            pass


        t = 0
        while 1:
            client = self.clients[t % len(self.clients)]

            client.is_turn = True

            client.sendCommand(Commands.TURN)
            self.send_else(client, f"{client.name}의 턴")

            while client.is_turn:
                pass
            t += 1

        # try:
        #     while len(self.clients) < 3:
        #         client_socket, client_addr = self.server.accept()

        #         client_init_thread = threading.Thread(target = self.client_initalize, args=(client_socket, client_addr))
        #         client_init_thread.run()

        # except Exception as e:
        #     print(f'Exception : {e}')

        # finally:
        #     self.log("서버가 더는 수락할 수 없음")

    def is_name_duplicated(self, name):
        for client in self.clients:
            if name == client.name:
                return True
        return False

    def client_init(self, client: Client):
        client.sendCommand(Commands.SET_NAME)
        while 1:
            data = client.recv()
            if not data:
                raise Exception("탈주")

            name = data.decode()

            if not self.is_name_duplicated(name):
                client.send(State.Available)
                client.name = name
                break
            else:
                client.send(State.Unavailable)

        client.setRandomResource()
        client.sendInfo()
        self.log(f"{client.name}님이 접속하셨습니다")
        self.send_else(client, f"{client.name}님이 접속하셨습니다")
        print(client.resource)
        self.clients.append(client)

    def client_process(self, client: Client):
        self.client_init(client)

        try:
            while 1:
                data = client.recv()
                if not data:
                    raise Exception("유저 탈주")

                if client.is_turn:
                    self.log(f"{client.name}: {data.decode()}")
                    client.is_turn = False

        except Exception as e:
            if client in self.clients:
                self.clients.remove(client)

            client.socket.close()

    def send_to(self, port, msg):
        for client in self.clients:
            if client.port == port:
                client.send(msg.encode())

    def send_else(self, this_client, msg):
        for client in self.clients:
            if client != this_client:
                client.send(msg)

    def log(self, msg: str):
        print(f"server log: {msg}")


ip = 'localhost'
port = 25565

tserver = TradingServer((ip, port))
tserver.start()
