import socket
import time
import struct
from random import randint
from threading import Thread
import os
from scapy.arch import get_if_addr

os.system("")


# Style to make our output fun to read.
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

# Global vars.
udpIp = '<broadcast>'
udpPort = 13117
tcpPort = 2004
counter = 0
endGame=False


# Start brodcasting searching for clients
def startBroadcast():
    global counter
    ip = '192.168.56.1'
    udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(style.UNDERLINE + "Server started, listening on IP address " + ip)

    while counter < 2:
            udpSocket.sendto(struct.pack('IBH', 0xabcddcba, 0x2, tcpPort), (udpIp, udpPort))
            time.sleep(1)

# Start connecting clients until 2 connected.
def connectClients():
    global counter
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
            handleGame(connect1, connect2)

# Running the actual game after 2 players connected.          
def handleGame(conn1, conn2):
    global counter, endGame
    team1 = conn1.recv(1024).decode()
    team2 = conn2.recv(1024).decode()
    num1 = randint(0, 9)
    num2 = randint(0, 9-num1)
    # Let's start the game!!!
    mathQuestion = "Welcome to Quick Maths.\nPlayer 1: " + team1 + "\nPlayer 2: " + team2 + "\n====\n Please answer the following question as fast as you can:\n" + "How much is: " + str(num1) +"+" + str(num2) +"?\n"
    conn1.sendall(mathQuestion.encode())
    conn2.sendall(mathQuestion.encode())
    gotAnswer = False
    endOfTime = time.time() + 10
    # Trying to find a winner for 10sec 
    while time.time() < endOfTime and gotAnswer is False:
        try:
            answer1 = conn1.recv(1024)
            if int(answer1) == num1+num2:
                endMessage = "Game over!\nThe correct answer was " + str(
                    num1+num2) + "!\nCongratulations to the winner1:" + team1
                gotAnswer = True
            else:
                endMessage = "Game over!\nThe correct answer was " + str(
                    num1+num2) + "!\nCongratulations to the winner2:" + team2
                gotAnswer = True
        except:
            try:
                answer2 = conn2.recv(1024)
                if int(answer2) == num1+num2:
                    endMessage = "Game over!\nThe correct answer was " + str(
                        num1+num2) + "!\nCongratulations to the winner3:" + team2
                    gotAnswer = True
                else:
                    endMessage = "Game over!\nThe correct answer was " + str(
                        num1+num2) + "!\nCongratulations to the winner4:" + team1
                    gotAnswer = True
            except:
                pass


    # Announcing the winner
    conn1.sendall(endMessage.encode())
    conn2.sendall(endMessage.encode())
    conn1.close()
    conn2.close()
    endGame = True
    # Game Over.





def main():
    global counter,endGame
    while endGame==False:
        # Starting the threads.
        broadcast = Thread(target=startBroadcast, args=())
        broadcast.setDaemon(True)
        broadcast.start()
        clients = Thread(target=connectClients, args=())
        clients.setDaemon(True)
        clients.start()
        broadcast.join()
        clients.join()
        counter = 0
        print("Game over, sending out offer requests...")


if __name__ == "__main__":
    main()