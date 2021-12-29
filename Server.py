import socket
import time
import struct
from random import randint
from threading import Thread
import os
from scapy.arch import get_if_addr

os.system("")


# Group of Different functions for different styles
class style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


udpIp = '<broadcast>'
udpPort = 13117
tcpPort = 2004
counter = 0
connect1 = None
connect2 = None

def startBordcast():
    global counter
    ip = '192.168.56.1'
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(style.UNDERLINE + "Server started, listening on IP address " + ip)

    while counter < 2:
            udpSocket.sendto(struct.pack('IBH', 0xabcddcba, 0x2, tcpPort), (udpIp, udpPort))
            time.sleep(1)

def connectClients():
    global connect1, connect2, counter
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpSocket.bind(('', tcpPort))
    tcpSocket.listen(2)
    while True:
        if counter < 2:
            try:
                conn, address = tcpSocket.accept()
                if counter == 0:
                    connect1 = conn
                else:
                    connect2 = conn

                counter += 1
            except Exception as e:
                pass

        else:
            time.sleep(10)
            break
def handleGame():
    global connect1,connect2,counter
    try:
        team1 = connect1.recv(1024).decode()
    except Exception as e:
        connect1.sendall('failed to get team name'.encode())
    try:
        team2 = connect2.recv(1024).decode()
    except Exception as e:
        connect1.sendall('failed to get team name'.encode())
    num1 = randint(0, 9)
    num2 = randint(0, 9-num1)
    mathQuestion = "Welcome to Quick Maths.\nPlayer 1: " + team1 + "\nPlayer 2: " + team2 + "\n====\n Please answer the following question as fast as you can:\n" + "How much is: " + str(num1) +"+" + str(num2) +"?\n"
    connect1.sendall(mathQuestion.encode())
    connect2.sendall(mathQuestion.encode())
    gotAnswer = False
    endOfTime = time.time() + 10
    while time.time() < endOfTime and gotAnswer == False:
        try:
            answer = connect1.recv(1024)
            if int(answer) == num1+num2:
                endMessage = "Game over!\nThe correct answer was " + str(
                    num1+num2) + "!\nCongratulations to the winner:" + team1
            else:
                endMessage = "Game over!\nThe correct answer was " + str(
                    num1+num2) + "!\nCongratulations to the winner:" + team2
            gotAnswer = True
        except:
            try:
                answer = connect2.recv(1024)
                if int(answer) == num1+num2:
                    endMessage = "Game over!\nThe correct answer was " + str(
                        num1+num2) + "!\nCongratulations to the winner:" + team2
                else:
                    gotAnswer = True
                    endMessage = "Game over!\nThe correct answer was " + str(
                        num1+num2) + "!\nCongratulations to the winner:" + team1
            except:
                time.sleep(0.1)
    connect1.sendall(endMessage.encode())
    connect2.sendall(endMessage.encode())







def main():
    global counter,connect1,connect2
    while True:
        broadcast = Thread(target=startBordcast(), args=())
        clients = Thread(target=connectClients(), args=())
        broadcast.start()
        clients.start()
        handleGame()

        counter = 0
        try:
            connect1.close()
            connect2.close()
        except:
            pass
        print("Game over, sending out offer requests...")

if __name__ == "__main__":
    main()