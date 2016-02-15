import socket

ip = '0.0.0.0'
port = 5880
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while True:
	data, addr = sock.recvfrom(1024)
	print 'Message:', data