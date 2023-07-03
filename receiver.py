from socket import *
from time import sleep
## No other imports allowed

from util import *


#Port # = 10100 + 4165995 % 500 = 10595
server_port = 10595
server_socket = socket(AF_INET, SOCK_DGRAM)
# bind the socket
server_socket.bind(('', server_port))
# packet num
pkt_num = 0
# previous packet sequence
prev_seq = -1

while True:
    msg, client_socket = server_socket.recvfrom(1024)
    pkt_num += 1
    print('packet num.' + str(pkt_num) + ' received: ', end='')
    print(msg)

    # Check if the packet is corrupted
    valid_msg = verify_checksum(msg)
    if pkt_num % 6 == 0:
        # packet loss
        print('simulating packet loss: sleep a while to trigger timeout event on the send side...')
        sleep(16)
    elif (not valid_msg) or pkt_num % 3 == 0:
        # packet corruption
        print('simulating packet bit errors/corrupted: ACK the previous packet!')
        response_packet = make_packet('', 1, prev_seq)
        server_socket.sendto(response_packet, client_socket)
    else:
        # The packet is well received
        print('packet is expected, message string delivered: ' + msg[12:].decode())
        print('packet is delivered, now creating and sending the ACK packet...')
        seq = msg[11] & 1
        response_packet = make_packet('', 1, seq)
        server_socket.sendto(response_packet, client_socket)
        prev_seq = seq
    print('all done for this packet!')
    print('\n\n')

