import sys
import socket
import struct

# Global vars.
udpPort = 13117

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

def main():
    print(style.RED + "Client started, listening for offer requests...")
    while True:
        # Start of setting udp.
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpSocket.bind(("", udpPort))
        # End of setting udp.
        try:
            # Start of setting tcp.
            tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            data, address = udpSocket.recvfrom(1024) # Data from udp socket.
            serverIp = str(address[0]) # Taking the ip from the address received.
            udpSocket.close() 
            magicCookie, type, tcpPort = struct.unpack('IBH', data)
            # Checking correct form of message. 
            if magicCookie != 0xabcddcba:
                print(style.RED + "Received a message without magic cookie failed to connect...")
            else:
                print(style.RED + "Received offer from " + serverIp + " attempting to connect...")
                # Connecting to the server and sending the him the team name.
                tcpSocket.connect((serverIp, tcpPort))
                teamname = input(style.CYAN + "Please enter your team name: ")
                tcpSocket.sendall(teamname.encode())
                # Receiving the question and trying to answer it
                print(style.CYAN + tcpSocket.recv(1024).decode())
                tcpSocket.settimeout(10)
                char = sys.stdin.readline()[0]
                try:
                    tcpSocket.sendall(char.encode())
                except:
                    tcpSocket.close()
                print(style.CYAN + tcpSocket.recv(1024).decode())
                tcpSocket.close()
                print(style.RED + "Server disconnected, listening for offer requests...")
        except:
                pass

if __name__ == '__main__':
    main()