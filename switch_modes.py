import socket

# Make the UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)
message = "Toggle Interactive Mode"

try:
    # Send the data
    sent = sock.sendto(message, server_address)

    # Get response
    data, server = sock.recvfrom(4096)

finally:
    sock.close()