import wx
from wx.lib.pubsub import pub
import ticTacToe
import rockPaperScissors
from client import *
from time import sleep


# signUp
class SignUp(wx.Frame):
    def __init__(self):  # create sign up frame
        wx.Frame.__init__(self, None, title="Sign Up", size=(430, 300),
                          pos=(185, 130))
        self.SetBackgroundColour((153, 255, 153))

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(40)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(100)

        lbl1 = wx.StaticText(self, label="Create an account")
        lbl1.SetFont(wx.Font(22, wx.ROMAN, wx.NORMAL, wx.BOLD))
        row.Add(lbl1)
        col.Add(row)

        col.AddSpacer(20)
        row6 = wx.BoxSizer(wx.HORIZONTAL)
        row6.AddSpacer(80)
        self.name = wx.TextCtrl(self, size=wx.Size(110, 22))
        self.name.Bind(wx.EVT_SET_FOCUS, self.remove_lbl3)
        row6.Add(self.name)
        row6.AddSpacer(45)
        lbl4 = wx.StaticText(self, label=":Nickname")
        lbl4.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row6.Add(lbl4)
        col.Add(row6)

        row7 = wx.BoxSizer(wx.HORIZONTAL)
        row7.AddSpacer(75)
        self.nicknameError = wx.StaticText(self)
        self.nicknameError.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.LIGHT))
        self.nicknameError.SetForegroundColour((255, 0, 0))  # set text color
        row7.Add(self.nicknameError)
        col.Add(row7)

        col.AddSpacer(5)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(80)
        self.user = wx.TextCtrl(self, size=wx.Size(110, 22))
        self.user.Bind(wx.EVT_SET_FOCUS, self.remove_lbl2)
        row1.Add(self.user)
        row1.AddSpacer(40)  # space between StaticText and TextCtrl
        lbl2 = wx.StaticText(self, label=":Username")
        lbl2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row1.Add(lbl2)
        col.Add(row1)

        row5 = wx.BoxSizer(wx.HORIZONTAL)
        row5.AddSpacer(70)
        self.usernameError = wx.StaticText(self)
        self.usernameError.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.LIGHT))
        self.usernameError.SetForegroundColour((255, 0, 0))  # set text color
        row5.Add(self.usernameError)
        col.Add(row5)

        col.AddSpacer(5)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(80)  # space between StaticText and TextCtrl
        self.password = wx.TextCtrl(self, size=wx.Size(110, 22),
                                    style=wx.TE_PASSWORD)
        row2.Add(self.password)
        row2.AddSpacer(42)  # space between StaticText and TextCtrl
        lbl4 = wx.StaticText(self, label=":Password")
        self.password.Bind(wx.EVT_SET_FOCUS, self.remove_lbl1)
        lbl4.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row2.Add(lbl4)
        col.Add(row2)

        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.AddSpacer(70)
        self.passwordError = wx.StaticText(self)
        self.passwordError.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.LIGHT))
        self.passwordError.SetForegroundColour((255, 0, 0))
        row3.Add(self.passwordError)
        col.Add(row3)

        col.AddSpacer(10)
        row4 = wx.BoxSizer(wx.HORIZONTAL)
        row4.AddSpacer(80)
        btn1 = wx.Button(self, label="sign up")
        btn1.Bind(wx.EVT_BUTTON, self.check)
        row4.Add(btn1)
        row4.AddSpacer(70)
        cancel = wx.Button(self, label="cancel")
        cancel.Bind(wx.EVT_BUTTON, self.cancel)
        row4.Add(cancel)
        col.Add(row4)

        self.SetSizer(col)
        self.Show()

        pub.subscribe(self.listener, "update3")  # create a pubsub receiver
        self.valid = ""

    def remove_lbl1(self, event):  # delete password error text
        self.passwordError.SetLabelText("")
        self.password.SetBackgroundColour("white")
        self.password.Clear()

    def remove_lbl2(self, event):  # delete username error text
        self.usernameError.SetLabelText("")
        self.user.SetBackgroundColour("white")
        self.user.Clear()

    def remove_lbl3(self, event):  # delete nickname error text
        self.nicknameError.SetLabelText("")
        self.name.SetBackgroundColour("white")
        self.name.Clear()

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[1] == "checkSignUp":  # sign up status
            self.valid = [info[2], info[3], info[4]]

    def check(self, event):  # Check if user can sign up
        p = self.password.GetValue()
        u = self.user.GetValue()
        n = self.name.GetValue()
        msg = "3,checkSignUp," + u + "," + n
        conn_q.put(msg)
        sleep(0.5)
        while self.valid == "":
            sleep(0.2)
            print("sleep")
        cond1 = len(p) < 4
        cond2 = len(u) < 4
        cond3 = len(n) > 8 or len(n) < 1
        if self.valid[0] == "True" and cond1 is False and cond2 is False \
                and cond3 is False:  # sign up succeeded
            msg = "3,insertUser," + u + "," + p + "," + n
            conn_q.put(msg)
            self.Destroy()
        else:
            if cond1:
                self.password.SetBackgroundColour("pink")
                self.password.Refresh()
                self.passwordError.SetLabelText("Use at least "
                                                "4 characters")
            if cond2 or self.valid[1] == "0":
                self.user.SetBackgroundColour("pink")
                self.user.Refresh()
                if cond2:
                    self.usernameError.SetLabelText("Use at least "
                                                    "4 characters")
                else:
                    self.usernameError.SetLabelText("Username is "
                                                    "already taken")
            if cond3 or self.valid[2] == "0":
                self.name.SetBackgroundColour("pink")
                self.name.Refresh()
                if cond3:
                    self.nicknameError.SetLabelText("Use 1-8 characters")
                else:
                    self.nicknameError.SetLabelText("Nickname is "
                                                    "already taken")

    def cancel(self, event):  # close sign up frame
        self.Close()


# chat
class Chat(wx.Frame):

    def __init__(self, name):  # create chat frame
        self.name = name
        wx.Frame.__init__(self, None, title="Chat", size=(500, 450),
                          pos=(150, 100))
        self.SetBackgroundColour('white')
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(30)

        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(100)
        self.messageBox = wx.TextCtrl(self, size=wx.Size(300, 260),
                                      style=wx.TE_MULTILINE | wx.HSCROLL)
        self.messageBox.SetEditable(False)
        row.Add(self.messageBox)
        col.Add(row)
        col.AddSpacer(30)

        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(70)
        send_btn = wx.Button(self, label='Send', size=wx.Size(80, 25))
        send_btn.Bind(wx.EVT_BUTTON, self.send_msg)
        row1.Add(send_btn)
        row1.AddSpacer(50)
        self.sendBox = wx.TextCtrl(self, size=wx.Size(200, 50))
        row1.Add(self.sendBox)
        col.Add(row1)

        self.SetSizer(col)
        self.Show()

        pub.subscribe(self.listener, "update4")  # create a pubsub receiver

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[1] == "msg":  # user got chat message
            self.messageBox.AppendText(info[2] + ":" + info[3] + '\n')

    def send_msg(self, event):  # send user's message
        msg1 = self.sendBox.GetValue()
        if msg1 != "":
            self.sendBox.Clear()
            msg = "4,msg," + self.name + "," + msg1
            conn_q.put(msg)
            self.messageBox.AppendText("You: " + msg1 + '\n')

    def on_erase_background(self, evt):  # add a picture to the background
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        image = wx.Image("chat.bmp", wx.BITMAP_TYPE_ANY)
        bmp = wx.Bitmap(image)
        dc.DrawBitmap(bmp, 0, 0)


# login
class Login(wx.Frame):
    def __init__(self):  # create login frame
        wx.Frame.__init__(self, None, title="Login", size=(430, 320),
                          pos=(185, 130))
        self.SetBackgroundColour((181, 253, 246))

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(60)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(80)

        lbl1 = wx.StaticText(self, label="login")
        lbl1.SetFont(wx.Font(22, wx.ROMAN, wx.NORMAL, wx.BOLD))
        row.Add(lbl1)
        col.Add(row)

        col.AddSpacer(20)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(80)
        self.user = wx.TextCtrl(self, size=wx.Size(110, 25))
        self.user.Bind(wx.EVT_SET_FOCUS, self.remove_lbl2)
        row1.Add(self.user)
        row1.AddSpacer(40)  # space between StaticText and TextCtrl
        lbl2 = wx.StaticText(self, label=":Username")
        lbl2.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row1.Add(lbl2)
        col.Add(row1)

        col.AddSpacer(10)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(80)  # space between StaticText and TextCtrl
        self.password = wx.TextCtrl(self, size=wx.Size(110, 25),
                                    style=wx.TE_PASSWORD)
        row2.Add(self.password)
        row2.AddSpacer(42)  # space between StaticText and TextCtrl
        lbl3 = wx.StaticText(self, label=":Password")
        self.password.Bind(wx.EVT_SET_FOCUS, self.remove_lbl1)
        lbl3.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.LIGHT))
        row2.Add(lbl3)
        col.Add(row2)

        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.AddSpacer(122)
        self.error = wx.StaticText(self)
        self.error.SetForegroundColour((255, 0, 0))
        row3.Add(self.error)
        col.AddSpacer(10)
        col.Add(row3)

        row4 = wx.BoxSizer(wx.HORIZONTAL)
        row4.AddSpacer(80)
        btn1 = wx.Button(self, label="Login")
        btn1.Bind(wx.EVT_BUTTON, self.login)
        row4.Add(btn1)

        row4.AddSpacer(25)  # space between StaticText and TextCtrl
        btn2 = wx.Button(self, label="Sign up")
        btn2.Bind(wx.EVT_BUTTON, self.sign_up)
        row4.Add(btn2)
        col.AddSpacer(20)
        col.Add(row4)

        self.SetSizer(col)
        self.Show()

        pub.subscribe(self.listener, "update2")  # create a pubsub receiver

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[1] == "checkLogin":  # login status
            if info[2] == "True":
                if info[4] == "1":
                    self.error.SetLabelText(".The user is already logged in")
                else:  # login succeeded
                    msg = "1,clientName" + "," + info[3]
                    conn_q.put(msg)
                    self.Close()
            else:
                self.error.SetLabelText(".Incorrect username or password")

    def login(self, event):  # send username and password
        u = self.user.GetValue()
        p = self.password.GetValue()
        msg = "2,checkLogin," + u + "," + p
        conn_q.put(msg)

    def sign_up(self, event):  # open sign up frame
        SignUp()
        self.user.Clear()
        self.password.Clear()
        self.error.SetLabelText("")

    def remove_lbl1(self, event):  # delete password error text
        self.error.SetLabelText("")
        self.password.Clear()

    def remove_lbl2(self, event):  # delete username error text
        self.error.SetLabelText("")
        self.user.Clear()


# MainFrame
class MainFrame(wx.Frame):
    name = ""

    def __init__(self):  # create main Frame (main menu)
        wx.Frame.__init__(self, None, title="CHAT PARTY", size=(500, 450),
                          pos=(150, 100))
        self.SetBackgroundColour('white')
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_CLOSE, self.close_frame)

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(60)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(150)  # space between StaticText and TextCtrl

        lbl1 = wx.StaticText(self, label="Chat party")
        lbl1.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))
        row.Add(lbl1)
        col.Add(row)

        col.AddSpacer(20)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(200)
        self.connect = wx.Button(self, label="connect")
        self.connect.SetBackgroundColour((112, 193, 249))
        self.connect.Bind(wx.EVT_BUTTON, self.connect_to_server)
        row1.Add(self.connect)
        col.Add(row1)

        col.AddSpacer(20)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(170)
        self.login = wx.Button(self, label="login", size=wx.Size(150, 70))
        self.login.SetBitmap(wx.Bitmap("login.bmp", wx.BITMAP_TYPE_ANY))
        self.login.SetBackgroundColour((255, 255, 255))
        self.login.Bind(wx.EVT_BUTTON, self.login1)
        self.login.Disable()
        row2.Add(self.login)
        col.Add(row2)

        col.AddSpacer(20)
        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.AddSpacer(170)
        self.signUp = wx.Button(self, label="Sign up", size=wx.Size(150, 70))
        self.signUp.SetBitmapLabel(wx.Bitmap("sign up.bmp",
                                             wx.BITMAP_TYPE_ANY))
        self.signUp.SetBackgroundColour((255, 255, 255))
        self.signUp.Bind(wx.EVT_BUTTON, self.sign_up1)
        self.signUp.Disable()
        row3.Add(self.signUp)
        col.Add(row3)

        self.SetSizer(col)
        self.Show()

    def close_frame(self, event):  # close frame
        print(" close frame")
        msg = "close"
        conn_q.put(msg)
        self.Destroy()

    def on_erase_background(self, evt):  # add a picture to the background
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        image = wx.Image("main.bmp", wx.BITMAP_TYPE_ANY)
        bmp = wx.Bitmap(image)
        dc.DrawBitmap(bmp, 0, 0)

    def connect_to_server(self, event):  # trying connect to the server
        comm_thread = Thread(target=client_send, args=())  # create tread
        comm_thread.start()
        pub.subscribe(self.listener, "update1")  # create a pubsub receiver

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[0] == "error":  # connection with server failed
            r = wx.MessageBox(info[1], "Connection error")
            if r == wx.OK:
                self.Destroy()

        else:
            info = tmp.split(",")
            if info[1] == "connect":   # connection with server succeeded
                self.connect.Hide()
                self.signUp.Enable()
                self.login.Enable()

            if info[1] == "clientName":  # get user's nickname
                MainFrame.name = info[2]
                self.login.Bind(wx.EVT_BUTTON, self.chat)
                self.login.SetLabel("chat")
                self.login.SetBackgroundColour('white')
                self.login.SetBitmapLabel(wx.Bitmap("gameIcon.bmp",
                                                    wx.BITMAP_TYPE_ANY))
                self.signUp.Bind(wx.EVT_BUTTON, self.game)
                self.signUp.SetBackgroundColour('white')
                self.signUp.SetBitmapLabel(wx.Bitmap("chatIcon.bmp",
                                                     wx.BITMAP_TYPE_ANY))
                self.signUp.SetLabel("games")

    def login1(self, event):  # open login frame
        Login()

    def sign_up1(self, event):  # open sign up frame
        SignUp()

    def chat(self, event):  # open chat frame
        Chat(MainFrame.name)

    def game(self, event):  # open games menu frame
        Games(MainFrame.name)


# games menu
class Games(wx.Frame):
    def __init__(self, name):  # create games menu frame
        self.name = name  # player's name
        self.rivalName = ""  # rival's name
        wx.Frame.__init__(self, None, -1, 'games menu', size=(500, 450),
                          pos=(150, 100))
        self.SetBackgroundColour('white')
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(50)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(80)

        lbl = wx.StaticText(self, label="choose a game to play")
        lbl.SetFont(wx.Font(22, wx.SWISS, wx.NORMAL, wx.BOLD))
        row.Add(lbl)
        col.Add(row)

        col.AddSpacer(40)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(110)
        self.xo = wx.Button(self, label="tic tac toe")
        self.xo.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.xo.Bind(wx.EVT_BUTTON, self.tic_tac_toe)
        row1.Add(self.xo)

        row1.AddSpacer(20)
        self.enter1 = wx.Button(self, label="enter game", size=wx.Size(70, 45))
        self.enter1.Bind(wx.EVT_BUTTON, self.open_xo)
        row1.Add(self.enter1)
        self.enter1.Disable()
        col.Add(row1)

        col.AddSpacer(40)
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(60)
        self.rps = wx.Button(self, label="rock paper scissors")
        self.rps.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.rps.Bind(wx.EVT_BUTTON, self.rock_paper_scissors)
        row2.Add(self.rps)

        row2.AddSpacer(20)
        self.enter2 = wx.Button(self, label="enter game", size=wx.Size(70, 45))
        self.enter2.Bind(wx.EVT_BUTTON, self.open_rps)
        row2.Add(self.enter2)
        self.enter2.Disable()
        col.Add(row2)

        self.SetSizer(col)
        self.Show()
        pub.subscribe(self.listener, "update5")  # create a pubsub receiver

    def on_erase_background(self, evt):  # add a picture to the background
        dc = evt.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        image = wx.Image("game.bmp", wx.BITMAP_TYPE_ANY)
        bmp = wx.Bitmap(image)
        dc.DrawBitmap(bmp, 0, 0)

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")
        if info[1] == "xo":
            if info[2] == "playing":
                wx.MessageBox("you are already in a game", "no")
                self.Destroy()
            else:  # user can connect to tic tac toe game
                self.rivalName = info[2]
                self.enter1.Enable()
                self.rps.Disable()
                self.xo.Disable()

        if info[1] == "rps":
            if info[2] == "playing":
                wx.MessageBox("you are already in a game", "no")
                self.Destroy()
            else:  # user can connect to rock paper scissors game
                self.rivalName = info[2]
                self.enter2.Enable()
                self.rps.Disable()
                self.xo.Disable()

    def open_xo(self, event):  # open tic tac toe frame
        ticTacToe.start(self.name, self.rivalName)
        self.Close()

    def open_rps(self, event):  # open rock paper scissors frame
        rockPaperScissors.start(self.name, self.rivalName)
        self.Close()

    def tic_tac_toe(self, event):  # trying open tic tac toe frame
        msg = "5,xo," + self.name
        conn_q.put(msg)

    # trying open rock paper scissors frame
    def rock_paper_scissors(self, event):  #
        msg = "5,rps," + self.name
        conn_q.put(msg)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
