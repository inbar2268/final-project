import wx
from gamesClient import *
from wx.lib.pubsub import pub


class XOPanel(wx.Panel):

    # create tic tac toe panel
    def __init__(self, parent, id, name, rival_name):
        self.rivalName = rival_name  # name of rival
        wx.Panel.__init__(self, parent, id)
        self.SetSize(500, 400)

        self.symbol = ""  # your symbol - x/o
        self.yourTurn = False  # your turn or not
        self.startGame = False  # game can start or not
        # list of the symbols and their places in the board [symbol,place(1-9)]
        self.xo = self.create_xo()
        # list of the locations in the board which the symbols can
        # be inserted [x0,y0,x1,y1]
        self.table = self.create_table()
        # places on the board where the symbols need to be placed [x,y]
        self.places = self.create_places()
        self.dc = wx.MemoryDC()  # when drawing not in OnPaint, use MemoryDC
        self.SetBackgroundColour("white")
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_UP, self.mouse_up)

        self.msg_lbl = wx.TextCtrl(self, size=wx.Size(325, 27),
                                   pos=(40, 375), style=wx.TE_CENTRE)
        self.msg_lbl.SetValue("Waiting for " + self.rivalName + " to connect")
        self.msg_lbl.SetEditable(False)
        self.msg_lbl.SetBackgroundColour('white')
        self.msg_lbl.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT))

        comm_thread = Thread(target=client_send, args=[9980])  # create thread
        comm_thread.start()
        pub.subscribe(self.listener, "update1")  # create a pubsub receiver

        msg = "1,addPlayer," + name + "," + rival_name
        conn_q.put(msg)

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        print(msg)
        if info[1] == "symbol":
            # player gets start status- symbol + if he starts
            self.symbol = str(info[2])
            if info[3] == "True":
                self.yourTurn = True
            if info[3] == "False":
                self.yourTurn = False
        if info[1] == "draw":  # rival draw on board
            place = int(info[2])
            symbol = str(info[3])
            self.xo[place - 1][0] = str(symbol)  # add symbol to xo list
            if self.symbol != symbol:
                self.yourTurn = True
                self.msg_lbl.SetValue("Your turn")
            self.redraw()
        if info[1] == "addPlayer":  # rival opened tic tac toe frame
            self.startGame = True
            if self.yourTurn is True:
                self.msg_lbl.SetValue("Your turn")
            else:
                self.msg_lbl.SetValue("not your turn")

        if info[1] == "rivalQuit":  # rival left the game
            self.msg_lbl.SetValue(self.rivalName + " left the game")
            self.yourTurn = False

    def on_paint(self, evt):  # draw board and updated symbols
        self.dc = wx.PaintDC(self)
        self.draw_board()
        for i in self.xo:  # draw symbols
            place = int(i[1])
            if i[0] != "":
                x = int(self.places[place - 1][0])
                y = int(self.places[place - 1][1])
                if i[0] == "x":
                    self.draw_x(x, y)
                else:
                    self.draw_o(x, y)

        a = self.check_row()
        if a[0] is True:  # one of the players won
            if a[1] == self.symbol:
                self.msg_lbl.SetValue("you are the winner")
            else:
                self.msg_lbl.SetValue(self.rivalName + " is the winner")
            self.win_line(a[2])
            self.yourTurn = False
        b = self.check_column()
        if b[0] is True:  # one of the players won
            if b[1] == self.symbol:
                self.msg_lbl.SetValue("you are the winner")
            else:
                self.msg_lbl.SetValue(self.rivalName + " is the winner")
            self.win_line(b[2])
            self.yourTurn = False
        c = self.check_diagonal()
        if c[0] is True:  # one of the players won
            if c[1] == self.symbol:
                self.msg_lbl.SetValue("you are the winner")
            else:
                self.msg_lbl.SetValue(self.rivalName + " is the winner")
            self.win_line(c[2])
            self.yourTurn = False

        tie = True
        for i in self.xo:
            if i[0] == "":
                tie = False

        if tie is True and a[0] is False and b[0] is False and c[0] is False:
            self.msg_lbl.SetValue("The game ended in a tie")

    def redraw(self):  # redraw the windows - create EVT_PAINT
        self.Hide()  # redraw the board
        self.Show()

    def mouse_up(self, e):  # player clicked on the frame
        x, y = e.GetPosition()
        ok = self.check_place(x, y)
        if ok[1] == 1 and self.yourTurn is True and self.startGame is True:
            self.xo[ok[0] - 1][0] = self.symbol
            msg = "1,draw," + str(ok[0]) + "," + self.symbol + \
                  "," + self.rivalName
            conn_q.put(msg)
            print("xo send: ", msg)
            self.yourTurn = False
            self.msg_lbl.SetValue("not your turn")
            self.redraw()

    def check_row(self):  # checking for a win
        win = False
        symbol = ""
        places_list = ()
        for i in range(0, 9, 3):
            if self.xo[i][0] == self.xo[i + 1][0] and self.xo[i + 1][0] == \
                    self.xo[i + 2][0] and self.xo[i][0] != "":
                win = True
                places_list = (self.xo[i][1], self.xo[i + 2][1])
                symbol = self.xo[i][0]
        return win, symbol, places_list

    def check_column(self):  # checking for a win
        win = False
        symbol = ""
        places_list = ()
        for i in range(3):
            if self.xo[i][0] == self.xo[i + 3][0] and self.xo[i + 3][0] == \
                    self.xo[i + 6][0] and self.xo[i][0] != "":
                win = True
                symbol = self.xo[i][0]
                places_list = (self.xo[i][1], self.xo[i + 6][1])
        return win, symbol, places_list

    def check_diagonal(self):  # checking for a win
        win = False
        symbol = ""
        places_list = ()
        if self.xo[0][0] == self.xo[4][0] and self.xo[4][0] == self.xo[8][0] \
                and self.xo[4][0] != "":
            win = True
            symbol = self.xo[4][0]
            places_list = (self.xo[0][1], self.xo[8][1])
        elif self.xo[2][0] == self.xo[4][0] and self.xo[4][0] == \
                self.xo[6][0] and self.xo[4][0] != "":
            win = True
            symbol = self.xo[4][0]
            places_list = (self.xo[2][1], self.xo[6][1])
        return win, symbol, places_list

    def win_line(self, places_list):  # draw a line on the winning symbols
        place1 = int(places_list[0])
        x0 = int(self.places[place1 - 1][0])
        y0 = int(self.places[place1 - 1][1])
        place2 = int(places_list[1])
        x1 = int(self.places[place2 - 1][0])
        y1 = int(self.places[place2 - 1][1])
        pen = wx.Pen(wx.Colour("black"), width=3)
        self.dc.SetPen(pen)
        self.dc.DrawLine(x0, y0, x1, y1)

    def draw_board(self):  # draw game's board
        # x0,y0,x1,y1
        pen = wx.Pen(wx.Colour("black"), width=5)
        self.dc.SetPen(pen)
        offset_x = 350
        offset_y = 350
        self.dc.DrawLine(offset_x, offset_y, offset_x - 300, offset_y)
        self.dc.DrawLine(offset_x, offset_y - 100, offset_x - 300,
                         offset_y - 100)
        self.dc.DrawLine(offset_x, offset_y - 200, offset_x - 300,
                         offset_y - 200)
        self.dc.DrawLine(offset_x, offset_y - 300, offset_x - 300,
                         offset_y - 300)

        self.dc.DrawLine(offset_x, offset_y - 300, offset_x, offset_y)
        self.dc.DrawLine(offset_x - 100, offset_y - 300, offset_x - 100,
                         offset_y)
        self.dc.DrawLine(offset_x - 200, offset_y - 300, offset_x - 200,
                         offset_y)
        self.dc.DrawLine(offset_x - 300, offset_y - 300, offset_x - 300,
                         offset_y)

    def draw_x(self, x, y):  # draw ix
        pen = wx.Pen(wx.Colour("GREEN"), width=10)
        self.dc.SetPen(pen)
        size = 20
        # x0,y1,x1,y0
        self.dc.DrawLine(x - size, y + size, x + size, y - size)
        self.dc.DrawLine(x - size, y - size, x + size, y + size)

    def draw_o(self, x, y):  # draw circle
        pen = wx.Pen(wx.Colour("RED"), width=10)
        self.dc.SetPen(pen)
        self.dc.DrawCircle(x, y, 25)

    def create_table(self):  # create table list
        table = []
        offset_x = 50
        offset_y = 50
        for i in range(3):
            for j in range(3):
                table.append([offset_x, offset_y, offset_x + 100,
                              offset_y + 100])
                offset_x = offset_x + 100
            offset_x = offset_x - 300
            offset_y = offset_y + 100
        return table

    def create_places(self):  # create places list
        places = []
        offset_x = 100
        offset_y = 100
        for i in range(3):
            for j in range(3):
                places.append([offset_x, offset_y])
                offset_x = offset_x + 100
            offset_x = offset_x - 300
            offset_y = offset_y + 100
        return places

    def create_xo(self):  # create xo list
        xo = []
        for i in range(9):
            xo.append(["", i + 1])
        return xo

    # check if player can insert his symbol into the board
    # (where he clicked)
    def check_place(self, x, y):
        pos = 0  # place in the board
        empty = True
        right_place = False
        for i in self.table:
            if (i[0] <= x <= i[2]) and (i[1] <= y <= i[3]):
                right_place = True
                break
            pos = pos + 1

        place = ""
        if right_place is True:
            place = pos + 1
            if self.xo[place - 1][0] == "x" or self.xo[place - 1][0] == "o":
                empty = False

        ok = empty * right_place
        list1 = (place, ok)
        return list1


class MainXo(wx.Frame):
    def __init__(self, name, rival_name):
        wx.Frame.__init__(self, None, -1, title="tic tac toe", size=(420, 470),
                          pos=(200, 30))
        self.rivalName = rival_name
        print(self.rivalName)
        XOPanel(self, -1, name, rival_name)
        self.Bind(wx.EVT_CLOSE, self.close_frame)
        self.Show(True)

    def close_frame(self, event):  # player closed the frame
        msg = "close," + self.rivalName
        conn_q.put(msg)
        wx.CallAfter(self.Destroy)


def start(name, rival_name):
    MainXo(name, rival_name)
