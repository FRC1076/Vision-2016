import socket

ip = '127.0.0.1'
port = 5880
message = raw_input('Input: ')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (ip, port))