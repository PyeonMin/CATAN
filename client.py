import socket
from _thread import *

HOST = '10.107.1.21'
PORT = 25565

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        print(f"\b\b\b{data.decode()}\n<< ", end="")


print('>> 연결됨')
nick = input('사용할 별명을 입력하세요:')
client_socket.send(nick.encode())

start_new_thread(recv_data, (client_socket,))

while True:
    message = input('<< ')
    if message == 'quit':
        close_data = message
        break

    client_socket.send(message.encode())

client_socket.close()