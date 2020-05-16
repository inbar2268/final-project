from socket import *
from socket import SHUT_WR
from threading import Thread
from wx.lib.pubsub import pub
from queue import Queue
from time import sleep

conn_q = Queue()


def client_recv(my_socket):
    while True:
        data = my_socket.recv(1024)
        if data == "":
            print("server close this socket")
            my_socket.close()
            break  # get out from thread
        data = data.decode('latin-1')

        tmp = data.split(",")
        if tmp[0] == "1":  # tic tac toe
            print ("client_recv:" + data)
            pub.sendMessage("update1", msg="server response " + data)
        if tmp[0] == "2":  # rock paper scissors
            print ("client_recv:" + data)
            pub.sendMessage("update2", msg="server response " + data)


def client_send(port):
    print("start client")
    my_socket = socket()
    my_socket.connect(("127.0.0.1", port))  # create socket

    recv_thread = Thread(target=client_recv, args=(my_socket,))
    recv_thread.start()

    while True:
        if conn_q.empty() is False:
            data = conn_q.get()
            print ("client_send:" + data)
            my_socket.sendall(data.encode('latin-1'))
            t = data.split(",")
            if t[0] == "close":
                print("close xo client")
                my_socket.shutdown(SHUT_WR)
                break
        sleep(0.05)  # sleep a little before check the queue again
