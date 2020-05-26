from socket import *
from threading import Thread
from wx.lib.pubsub import pub
from queue import Queue
from time import sleep
from socket import SHUT_RD

conn_q = Queue()


def client_recv(my_socket):
    while True:
        try:
            data = my_socket.recv(1024)
        except:
            break
        if data == "":
            print("server close this socket")
            my_socket.close()
            break  # get out from thread
        data = data.decode('latin-1')
        print("client receive:" + data)

        # 1-main 2-login 3-sighUp 4-chat 5-games menu
        tmp = data.split(",")
        if tmp[0] == "1":
            pub.sendMessage("update1", msg="server response " + data)
        if tmp[0] == "2":
            pub.sendMessage("update2", msg="server response " + data)
        if tmp[0] == "3":
            pub.sendMessage("update3", msg="server response " + data)
        if tmp[0] == "4":
            pub.sendMessage("update4", msg="server response " + data)
        if tmp[0] == "5":
            pub.sendMessage("update5", msg="server response " + data)
        if tmp[0] == "6":
            pub.sendMessage("update6", msg="server response " + data)


def client_send():
    print("start client")
    my_socket = socket()
    f = open('configu.txt', 'r')
    ip = f.read()
    f.close

    try:
        my_socket.connect((str(ip), 1233))  # create socket
        recv_thread = Thread(target=client_recv, args=(my_socket,))
        recv_thread.start()
    except Exception as msg:
        print("Socket Error: %s" % msg)
        # publish to update1
        pub.sendMessage("update1", msg="server response " +
                                       "error," + str(msg))

    while True:
        if not conn_q.empty():
            data = conn_q.get()
            print ("client_send:" + data)
            try:
                my_socket.sendall(data.encode('latin-1'))
            except Exception:
                print("Socket Error")

            if data == "close":
                print("client closed the socket")
                my_socket.shutdown(SHUT_RD)
                my_socket.close()
                break
        sleep(0.05)  # sleep a little before check the queue again
