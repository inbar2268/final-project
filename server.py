import socket
from threading import Thread
import _thread
import sqlite3

import xoServer
import rpsServer
import users1


class HandleClient(Thread):
    # class variable
    clientsAndNames = []  # list of sockets and nicknames
    clients = []  # list of sockets
    game1 = None  # user waits to connect to tic tac toe game
    game1open = False  # tic tac toe server opened
    game2 = None  # user waits to connect to rock paper scissors game
    game2open = False  # rock paper scissors server opened

    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket
        HandleClient.clients.append(client_socket)
        # connect to data base
        self.conn = sqlite3.connect('users.db', timeout=10,
                                    check_same_thread=False)
        self.users = users1.Users(self.conn)  # data base table
        data = "1,connect"
        self.client_socket.send(data.encode('ascii'))

    def run(self):
        while 1:
            try:
                client_info = self.client_socket.recv(1024)
            except Exception as msg:
                print("Socket Error: %s" % msg)
                break

            client_info_str = client_info.decode('ascii')
            print("server got: " + client_info_str)

            # if client closed the socket
            if client_info_str == "close" or client_info_str == "":
                print("client close the socket")
                HandleClient.clients.remove(self.client_socket)
                self.client_socket.close()
                self.close_client(self.client_socket)
                break

            msg = client_info_str.split(",")

            if msg[1] == "msg":  # user sent chat message
                HandleClient.broadcast(client_info, self.client_socket)

            elif msg[1] == "xo":  # user is trying connect to tic tac toe game
                playing = False
                cursor = self.conn.execute("SELECT * from USERS")
                for row in cursor:
                    if row[2] == msg[2]:
                        if row[4] == "1":  # check if user is already playing
                            playing = True
                            data = "5,xo,playing"
                            print("server sent: " + data)
                            self.client_socket.send(data.encode('ascii'))

                if playing is False:
                    if HandleClient.game1 is not None:
                        # user can connect to the game
                        if HandleClient.game1[0] != self.client_socket:
                            data1 = client_info_str
                            HandleClient.game1[0].send(data1.encode('ascii'))
                            data2 = "5,xo," + HandleClient.game1[1]
                            self.client_socket.send(data2.encode('ascii'))
                            HandleClient.game1 = None
                            if HandleClient.game1open is False:
                                _thread.start_new_thread(xoServer.start_server,
                                                         ())
                                HandleClient.game1open = True
                    else:
                        name = msg[2]
                        HandleClient.game1 = [self.client_socket, name]
                        if HandleClient.game1 == HandleClient.game2:
                            HandleClient.game2 = None

            elif msg[1] == "rps":
                # user is trying connect to rock paper scissors game
                playing = False
                cursor = self.conn.execute("SELECT * from USERS")
                for row in cursor:
                    if row[2] == msg[2]:
                        if row[4] == "1":  # check if user is already playing
                            playing = True
                            data = "5,rps,playing"
                            print("server sent: " + data)
                            self.client_socket.send(data.encode('ascii'))

                if playing is False:
                    if HandleClient.game2 is not None:
                        # user can connect to the game
                        if HandleClient.game2[0] != self.client_socket:
                            data1 = client_info_str
                            HandleClient.game2[0].send(data1.encode('ascii'))
                            data2 = "5,rps," + HandleClient.game2[1]
                            self.client_socket.send(data2.encode('ascii'))
                            HandleClient.game2 = None
                            if HandleClient.game2open is False:
                                _thread.start_new_thread(
                                    rpsServer.start_server, ())
                                HandleClient.game2open = True
                    else:
                        name = msg[2]
                        HandleClient.game2 = [self.client_socket, name]
                        if HandleClient.game1 == HandleClient.game2:
                            HandleClient.game1 = None

            else:
                if msg[1] == "checkLogin":  # user is trying to login
                    u_and_p = (msg[2], msg[3])
                    data = msg[0] + ",checkLogin," + str(self.check1(u_and_p))

                if msg[1] == "checkSignUp":  # user is trying to sign up
                    valid = self.check2(msg[2], msg[3])
                    aa = str(valid[0])
                    bb = str(valid[1])
                    cc = str(valid[2])
                    data = msg[0] + ",checkSignUp," + aa + "," + bb + "," + cc

                if msg[1] == "insertUser":  # insert new user to data base
                    self.users.insert_user(msg[2], msg[3], msg[4])
                    data = msg[0] + ",ok"

                if msg[1] == "clientName":  # get user's nickname
                    data = client_info_str
                    name = msg[2]
                    n = [self.client_socket, name]
                    HandleClient.clientsAndNames.append(n)

                print("server got: " + str(client_info_str))
                print("server sent: " + str(data))
                self.client_socket.send(data.encode('ascii'))

    @classmethod
    def broadcast(cls, msg, client_socket):  # send message to all the clients
        for sock in cls.clients:
            if sock != client_socket:
                sock.send(msg)

    def check1(self, tup):  # check login
        # executes an SQL statement.
        cursor = self.conn.execute("SELECT * from USERS")
        exist = False
        name = ""
        online = ""
        for row in cursor:
            if row[0] == tup[0] and row[1] == tup[1]:
                exist = True
                name = row[2]
                online = row[3]
                if row[3] == '0':
                    self.users.update_online(name, '1')
        data = str(exist) + "," + name + "," + online
        return data

    def check2(self, user, name):  # check sign up
        cursor = self.conn.execute("SELECT * from USERS")
        valid = True
        name_valid = 1
        user_valid = 1
        for row in cursor:
            if row[0] == user:
                valid = False
                user_valid = 0
            if row[2] == name:
                valid = False
                name_valid = 0
        t = [valid, user_valid, name_valid]
        return t

    # remove client from clientsAndNames list and update data base
    def close_client(self, client_socket):
        for i in HandleClient.clientsAndNames:
            if i[0] == client_socket:
                self.users.update_online(i[1], '0')
                HandleClient.clientsAndNames.remove(i)


class Server:
    def __init__(self, port):
        self.server_socket = socket.socket()  # create server socket
        try:
            self.server_socket.bind(('0.0.0.0', port))
        except Exception as msg:
            print("Socket Error: %s" % msg)
        self.server_socket.listen(5)

    def go(self):
        while 1:
            (client_socket, client_address) = self.server_socket.accept()
            aa = HandleClient(client_socket)
            aa.start()


a = Server(1233)
a.go()
