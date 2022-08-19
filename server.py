import socket
from _thread import *
import os

def send_else(client, msg):
    for socket in client_sockets:
        if socket != client:
            socket.send(msg.encode())


def threaded(client, addr):
    def escape():
        if addr[1] in client_names:
            print(f'>> 탈주: {client_names[addr[1]]}:{addr[1]}')
        else:
            print(f'>> 탈주: {addr[0]}:{addr[1]}')

    print('>> Connected by :', addr[0], ':', addr[1])

    is_named = False
    while True:
        try:
            data = client.recv(1024)
            if not data:
                escape()
                break

            data = data.decode()

            if not is_named:
                client_names[addr[1]] = data
                is_named = True
                send_else(client, f"{client_names[addr[1]]}님이  접속하셨습니다")

            else:
                print(f'>> {client_names[addr[1]]}({addr[1]}):{data}')
                send_else(client, f"{client_names[addr[1]]}:{data}")

        except ConnectionResetError as e:
            escape()
            break

    if client in client_sockets:
        client_sockets.remove(client)
        print('remove client list : ', len(client_sockets))

    client.close()


client_sockets = []
client_names = {}

# 서버 IP 및 열어줄 포트
HOST = '10.107.1.21'
PORT = 25565                                                 

# 서버 소켓 생성
print('>> Server Start')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))
        print("접속자 수 : ", len(client_sockets))

except Exception as e:
    print(f'Exception : {e}')

finally:
    server_socket.close()
