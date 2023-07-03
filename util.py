def create_checksum(packet_wo_checksum):
    checksum = 0

    # Divide the data into sets consisting of two bytes each, and subsequently calculate the total sum of the grouped data.
    for index in range(0, len(packet_wo_checksum), 2):
        if index + 1 >= len(packet_wo_checksum):
            checksum += (packet_wo_checksum[index] << 8) + 0
        else:
            checksum += (packet_wo_checksum[index] << 8) + packet_wo_checksum[index + 1]

    # Incorporate the carryout from the highest-valued bit into the outcome.
    checksum = (checksum & 0xffff) + (checksum >> 16)

    # 1's complement of sum
    checksum = (~checksum) & 0xffff

    return checksum.to_bytes(2, "big")


def verify_checksum(packet):
    checksum = 0

    # Divide the data into sets consisting of two bytes each, and subsequently calculate the total sum of the grouped data.
    for index in range(0, len(packet), 2):
        if index + 1 >= len(packet):
            checksum += (packet[index] << 8) + 0
        else:
            checksum += (packet[index] << 8) + packet[index + 1]

    # Incorporate the carryout from the highest-valued bit into the outcome.
    checksum = (checksum & 0xffff) + (checksum >> 16)

    # 1's complement of sum
    checksum = (~checksum) & 0xffff

    return checksum == 0


def make_packet(data_str, ack_num, seq_num):
    #create the 11th and 12th bytes
    length = 12 + len(data_str)
    length = (length << 1) + ack_num
    length = (length << 1) + seq_num
    length = length.to_bytes(2, "big")

    # create header of the packet
    header = 'COMPNETW'.encode()
    
    # get checksum
    checksum = create_checksum(header + length + data_str.encode())

    # return packet
    return header + checksum + length + data_str.encode()
