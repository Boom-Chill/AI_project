import socket
import re
from os import system
import socket
import whatBot

HOST = ''
PORT = 14003
while(True):
    choice = input(
        "\n-----HOST-----\n1. my HOST\n2. teacher HOST\n3. another HOST\n> ")
    if(choice == '1'):
        HOST = socket.gethostbyname(socket.gethostname())
        break
    if(choice == '2'):
        HOST = "209.97.169.233"
        break
    if(choice == '3'):
        HOST = input("Enter host: ")
        break

match = int(input("\nEnter match: "))

win = 0
lose = 0

for i in range(match):
    color = None
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        while True:
            ret = str(sock.recv(1024), "ASCII")
            if re.match("^victory_cell", ret) is None:
                if ret.split("\n")[-2] == color:
                    win += 1
                else:
                    lose += 1
                sock.close()
                break
            else:
                if color is None:
                    color = ret.split('\n')[-2]
                # system("cls")
                print(f"Match Number: {i + 1}")
                # ret is board
                print(ret)
                sock.sendall(bytes(whatBot.callBot(ret), "ASCII"))

total = match
print(f"Total matches: {total}")
print(f"wins: {win}")
print(f"loses: {lose}")
print(f"Winrate: {((win)*100/total)} %")
