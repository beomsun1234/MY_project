from socket import * 
import rospy
import move_base_pure_puresuit as m
import my_lane_detect as l
import gogo as g
import gogo2 as g2
import time
server_sock = socket(AF_INET,SOCK_STREAM) 
server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
server_sock.bind(("192.168.43.174", 8080)) 
server_sock.listen(1) 
print("wait") 
client_sock, addr = server_sock.accept()
print('Connected by', addr) 
data = client_sock.recv(1024).decode("utf-8")
data = data[2:]
print(data)
data2 ="finsh"
rospy.init_node('control', anonymous=True)
while True: 
    if data == 'parking':
        print("parking going")
        g.mycar().play()
        print("parking:",data2)
        client_sock.send(data2.encode())
        data = client_sock.recv(1024).decode("utf-8")
        data = data[2:]
        print(data)
        client_sock.close()
    elif data == 'lane':
        print("lane_detection going")
        g2.Lane_mycar().play()
        print("lane_detection:",data2)
        client_sock.send(data2.encode())
        data = client_sock.recv(1024).decode("utf-8")
        data = data[2:]
        print(data)
        client_sock.close()
    elif data == 'cruise':
        print("cruise mode going")
        m.pure_pursuit()      
        print("GOAL Reached!")
        client_sock.send(data2.encode())
        data = client_sock.recv(1024).decode("utf-8")
        data = data[2:]
        client_sock.close()
    if data == 'finsh': ##  socet reconnection
        client_sock, addr = server_sock.accept()
        data = client_sock.recv(1024).decode("utf-8")
        data = data[2:]

client_sock.close() 
server_sock.close()
