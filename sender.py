from socket import *
from util import *

class Sender:
    def __init__(self):
        """ 
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
        
        Please check the main.py for a reference of how your function will be called.
        """
        # packet num
        self.__packet_num = 0
        # sequence num
        self.__seq_num = 0

    def send_pkt(self, pkt, app_msg_str):
        client_socket = socket(AF_INET, SOCK_DGRAM)
       
       #set timeout
        client_socket.settimeout(15)

        #send packet
        #Port# = 10100 + 4165995 % 500 = 10595
        receiver = ('localhost', 10595)
        client_socket.sendto(pkt, receiver)
        self.__packet_num += 1

        print('packet num.' + str(self.__packet_num) + ' is successfully sent to the receiver.')

        try:
            # receive message from receiver
            msg, server_socket = client_socket.recvfrom(1024)
            # get ack number
            ack = msg[11] & 1
            if self.__seq_num == ack:
                # packet is received correctly
                print('packet is received correctly: seq.num ' + str(self.__seq_num) + ' = ' + 'ACK num ' + str(ack) + '. all done!')
                print('\n\n')
                self.__seq_num = 0 if self.__seq_num == 1 else 1
            else:
                # packet is corrupted
                print('receiver acked the previous pkt, resend!')
                print('\n\n')
                print('[ACK-Previous retransmission]: ' + app_msg_str)
                self.send_pkt(pkt, app_msg_str)
            client_socket.close()
        except Exception as err:
            print('socket timeout! Resend!')
            print('\n\n')
            print('[timeout retransmission]: ' + app_msg_str)
            self.send_pkt(pkt, app_msg_str)

    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)

      Args:
        app_msg_str: the message string (to be put in the data field of the packet)

      """
        print('original message string: ' + app_msg_str)

        # always generate packet with ack# is 0
        pkt = make_packet(app_msg_str, 0, self.__seq_num)

        #print the information of the packet
        print('packet created: ', end='')
        print(pkt)
        
        #send the packet to the receiver side
        self.send_pkt(pkt, app_msg_str)