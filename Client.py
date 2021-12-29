import sys
import socket
import struct

udpPort = 13117

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

def main():
    print(style.RED + "Client started, listening for offer requests...")
    while True:
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpSocket.bind(("", udpPort))
        try:
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            data, address = udpSocket.recvfrom(1024)
            serverIp = str(address[0])
            udpSocket.close()
            magicCookie, type, tcpPort = struct.unpack('IBH', data)
            if magicCookie != 0xabcddcba:
                print(style.RED + "Received a message without magic cookie failed to connect...")
            else:
                print(style.RED + "Received offer from " + serverIp + " attempting to connect...")
            tcpSocket.connect((serverIp, tcpPort))
            teamname = input(style.CYAN + "Please enter your team name: ")
            tcpSocket.sendall(teamname.encode())
            sys.stdout.write(style.CYAN + tcpSocket.recv(1024).decode())
            tcpSocket.settimeout(10)
            char = sys.stdin.readline()[0]
            try:
                tcpSocket.sendall(char.encode())
            except:
                tcpSocket.close()
            print(tcpSocket.recv(1024).decode())
            tcpSocket.close()
            print(style.RED + "Server disconnected, listening for offer requests...")
        except:
            pass

if __name__ == '__main__':
    main()