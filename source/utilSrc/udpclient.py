import socket
import time
UDP_IP = "192.168.0.103"
# UDP_IP = "127.0.0.1"
UDP_PORT = 1234
MESSAGE = b"bed"
 
print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP


# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

sock.sendto(bytes(str("99"), "utf-8"), (UDP_IP, UDP_PORT))

while True:
    for i in range(0, 99):
        
        sock.sendto(bytes(str(i), "utf-8"), (UDP_IP, UDP_PORT))
        time.sleep(1)

    sock.sendto(bytes(str("99"), "utf-8"), (UDP_IP, UDP_PORT))  
    time.sleep(8) 
    sock.sendto(bytes(str("bed"), "utf-8"), (UDP_IP, UDP_PORT)) 
    time.sleep(8) 

    sock.sendto(bytes(str("wait"), "utf-8"), (UDP_IP, UDP_PORT))
    time.sleep(8) 
