import socket
from threading import Thread
import sqlite3
import users1


class HandleClient(Thread):
    # class variable
    clientsAndNames = []  # list of sockets and nicknames
    clients = []  # list of sockets

    def __init__(self, client_socket):
        Thread.__init__(self)
        self.client_socket = client_socket
        HandleClient.clients.append(client_socket)
        # connect to data base
        self.conn1 = sqlite3.connect('users.db', timeout=10,
                                     check_same_thread=False)
        self.users = users1.Users(self.conn1)  # data base table

        self.conn2 = sqlite3.connect('wins.db', timeout=10,
                                     check_same_thread=False)
        self.wins = users1.Wins(self.conn2)  # data base table

    def run(self):
        while 1:
            client_info = self.client_socket.recv(1024)
            client_info_str = client_info.decode('ascii')
            print("server got: " + client_info_str)

            if client_info_str == "":
                self.client_socket.close()
                print("client close the socket")
                for i in HandleClient.clients:
                    if i == self.client_socket:
                        HandleClient.clients.remove(self.client_socket)
                for i in HandleClient.clientsAndNames:
                    if i[0] == self.client_socket:
                        HandleClient.clientsAndNames.remove(i)
                        break
                break

            msg = client_info_str.split(",")

            if msg[0] == "close":  # client closed the socket
                a = HandleClient.clients
                if self.client_socket in a:
                    HandleClient.clients.remove(self.client_socket)
                b = HandleClient.clientsAndNames
                for i in b:
                    if i[0] == self.client_socket:
                        self.users.update_play(i[1], '0')
                        HandleClient.clientsAndNames.remove(i)
                        break
                for i in HandleClient.clientsAndNames:
                    if i[1] == msg[1]:
                        data = "2,rivalQuit"
                        i[0].send(data.encode('ascii'))
                        print("server sent: " + data)
                        break
                break

            if msg[1] == "addPlayer":
                # player opened rock paper scissors frame
                HandleClient.clientsAndNames.append([self.client_socket,
                                                     msg[2]])
                self.users.update_play(msg[2], '1')
                HandleClient.broadcast(client_info, self.client_socket)
                for i in range(len(HandleClient.clientsAndNames)):
                    if HandleClient.clientsAndNames[i][1] == msg[3]:
                        data = "2,addPlayer," + msg[3] + "," + msg[2]
                        self.client_socket.send(data.encode('ascii'))

            if msg[1] == "choose":  # player chose a symbol
                for i in HandleClient.clientsAndNames:
                    found = False
                    if i[1] == msg[4]:
                        found = True
                        i[0].send(client_info_str.encode('ascii'))
                        print("server sent: " + client_info_str)
                        break
                if found is False:
                    data = "2,rivalQuit"
                    self.client_socket.send(data.encode('ascii'))

            if msg[1] == "madeAChoice":  # player made a choice
                for i in HandleClient.clientsAndNames:
                    found = False
                    if i[1] == msg[2]:
                        found = True
                        i[0].send(client_info_str.encode('ascii'))
                        print("server sent: " + client_info_str)
                        break
                if found is False:
                    data = "2,rivalQuit"
                    self.client_socket.send(data.encode('ascii'))

            if msg[1] == "newRound":  # new round begins
                for i in HandleClient.clientsAndNames:
                    found = False
                    if i[1] == msg[2]:
                        found = True
                        i[0].send(client_info_str.encode('ascii'))
                        print("server sent: " + client_info_str)
                        break
                if found is False:
                    data = "2,rivalQuit"
                    self.client_socket.send(data.encode('ascii'))

            if msg[1] == "win":  # player won the game
                for i in HandleClient.clientsAndNames:
                    if i[0] == self.client_socket:
                        self.update(i[1])
                        break

    @classmethod
    def broadcast(cls, msg, client_socket):  # send message to all the clients
        for sock in cls.clients:
            if sock != client_socket:
                sock.send(msg)

    def update(self, name):  # update nums of wins
        cursor = self.conn2.execute("SELECT * from WINS")
        for row in cursor:
            if row[0] == name:
                print("found name:" + name)
                win = int(row[2]) + 1
                print(win)
                self.wins.update_rock_paper_scissors(name, str(win))
                print("win= " + str(win))


class Server:
    def __init__(self, port):
        self.server_socket = socket.socket()  # create server socket
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)

    def go(self):
        while 1:
            (client_socket, client_address) = self.server_socket.accept()
            a = HandleClient(client_socket)
            a.start()


def start_server():
    a = Server(4532)
    print("server rock paper scissors")
    a.go()
