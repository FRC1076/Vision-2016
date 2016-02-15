import sys
import socket

if len(sys.argv) > 1:
	ip = sys.argv[1]
else:
	ip = '172.16.1.63'

port = 5880
message = raw_input('Input: ')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(message, (ip, port))