import wx
from gamesClient import *
from time import sleep


class MainRps(wx.Frame):
    score = 0  # player's score
    rScore = 0  # rival's score
    # rock=1 paper=2 scissors=3
    symbol = ""  # player's symbol
    rSymbol = ""  # rival's symbol
    round = 1  # number of rounds
    youChose = False  # player chose a symbol or not
    rivalChose = False  # rival chose a symbol or not
    choiceMsg = ""  # player's choice message
    result = ""  # round result message

    def __init__(self, name, rival_name):  # create rock paper scissors frame
        wx.Frame.__init__(self, None, -1, 'rock paper scissors',
                          size=(420, 470), pos=(200, 30))

        self.name = name  # player's name
        self.rivalName = rival_name  # rival's name
        self.Bind(wx.EVT_CLOSE, self.close_frame)
        self.SetBackgroundColour((179, 217, 255))

        col = wx.BoxSizer(wx.VERTICAL)
        col.AddSpacer(20)

        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.AddSpacer(155)
        lbl = "ROUND " + str(MainRps.round)
        self.roundNumber = wx.StaticText(self, label=lbl)
        self.roundNumber.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        row2.Add(self.roundNumber)
        col.Add(row2)

        col.AddSpacer(5)
        row3 = wx.BoxSizer(wx.HORIZONTAL)
        row3.AddSpacer(50)
        you = wx.TextCtrl(self, size=wx.Size(110, 22), style=wx.TE_CENTRE)
        you.SetValue("you")
        you.SetEditable(False)
        you.SetBackgroundColour((179, 217, 255))
        you.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        row3.Add(you)
        row3.AddSpacer(10)
        self.yourScore = wx.StaticText(self, label=str(MainRps.score))
        self.yourScore.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.LIGHT))
        self.yourScore.SetBackgroundColour((255, 255, 255))
        row3.Add(self.yourScore)
        row3.AddSpacer(25)

        self.rivalScore = wx.StaticText(self, label=str(MainRps.rScore))
        self.rivalScore.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.LIGHT))
        self.rivalScore.SetBackgroundColour((255, 255, 255))
        row3.Add(self.rivalScore)
        row3.AddSpacer(10)
        rival = wx.TextCtrl(self, size=wx.Size(110, 22), style=wx.TE_CENTRE)
        rival.SetValue(self.rivalName)
        rival.SetEditable(False)
        rival.SetBackgroundColour((179, 217, 255))
        rival.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD))
        row3.Add(rival)
        col.Add(row3)

        col.AddSpacer(20)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.AddSpacer(55)  # space between StaticText and TextCtrl
        lbl1 = wx.StaticText(self, label="Choose rock/ paper/ scissors")
        lbl1.SetFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        row.Add(lbl1)
        col.Add(row)

        col.AddSpacer(10)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(80)  # space between StaticText and TextCtrl

        self.rock = wx.Button(self, size=wx.Size(60, 92))
        self.rock.SetBitmap(wx.Bitmap("rock.bmp", wx.BITMAP_TYPE_ANY))
        self.rock.Bind(wx.EVT_BUTTON, self.add_rock)
        self.rock.Disable()
        row1.Add(self.rock)
        row1.AddSpacer(30)

        self.paper = wx.Button(self, size=wx.Size(60, 92))
        self.paper.SetBitmap(wx.Bitmap("paper.bmp", wx.BITMAP_TYPE_ANY))
        self.paper.Bind(wx.EVT_BUTTON, self.add_paper)
        self.paper.Disable()
        row1.Add(self.paper)
        row1.AddSpacer(30)

        self.scissors = wx.Button(self, size=wx.Size(60, 92))
        self.scissors.SetBitmap(wx.Bitmap("scissors.bmp", wx.BITMAP_TYPE_ANY))
        self.scissors.Bind(wx.EVT_BUTTON, self.add_scissors)
        self.scissors.Disable()
        row1.Add(self.scissors)
        col.Add(row1)

        col.AddSpacer(10)
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        row1.AddSpacer(30)

        box = wx.StaticText(self, pos=(50, 250), size=wx.Size(300, 150))
        box.SetBackgroundColour((255, 255, 255))

        self.msg_lbl = wx.TextCtrl(self, size=wx.Size(250, 25), pos=(75, 260),
                                   style=wx.TE_CENTRE)
        self.msg_lbl.SetValue("Waiting for " + self.rivalName + " to connect")
        self.msg_lbl.SetEditable(False)
        self.msg_lbl.SetBackgroundColour((255, 255, 255))
        self.msg_lbl.SetFont(wx.Font(11, wx.SWISS, wx.NORMAL, wx.LIGHT))

        self.you_lbl = wx.StaticText(self, label="", pos=(70, 285))
        self.you_lbl.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT))
        self.you_lbl.SetBackgroundColour((255, 255, 255))

        self.rival_lbl = wx.StaticText(self, label="", pos=(255, 285))
        self.rival_lbl.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.LIGHT))
        self.rival_lbl.SetBackgroundColour((255, 255, 255))

        self.bitmap1 = wx.StaticBitmap(self, pos=(75, 310))
        self.bitmap1.Hide()
        self.bitmap2 = wx.StaticBitmap(self, pos=(270, 310))
        self.bitmap2.Hide()

        self.SetSizer(col)
        self.Show()

        comm_thread = Thread(target=client_send, args=[4532])  # create thread
        comm_thread.start()
        pub.subscribe(self.listener, "update2")  # create a pubsub receiver

        msg = "2,addPlayer," + name + "," + rival_name
        conn_q.put(msg)

    def listener(self, msg):  # Listener function - Receives update messages
        t = msg
        tmp = t[len("server response") + 1:]
        info = tmp.split(",")

        if info[1] == "addPlayer":  # rival opened rock paper scissors frame
            self.enable_buttons()
            self.msg_lbl.SetLabelText("Wait for you to choose")

        if info[1] == "rivalQuit":  # rival left the game
            lbl = self.rivalName + " left the game"
            self.msg_lbl.SetLabelText(lbl)
            self.disable_buttons()

        if info[1] == "madeAChoice":  # rival chose a symbol
            MainRps.rivalChose = True
            if MainRps.youChose is True:
                conn_q.put(MainRps.choiceMsg)
                MainRps.choiceMsg = ""
                MainRps.youChose = False
                MainRps.rivalChose = False

        if info[1] == "choose":  # rival's choice + score
            MainRps.rScore = int(info[3])
            MainRps.rSymbol = info[2]
            MainRps.result = self.check()
            if MainRps.result == "":
                MainRps.result = "It's a tie"
            MainRps.round = MainRps.round + 1

            self.update()

    def add_rock(self, event):  # player clicked rock button
        self.add_symbol("1")

    def add_paper(self, event):  # player clicked paper button
        self.add_symbol("2")

    def add_scissors(self, event):  # player clicked scissors button
        self.add_symbol("3")

    def add_symbol(self, symbol):
        self.disable_buttons()
        lbl = "Wait for " + self.rivalName + " to choose"
        self.msg_lbl.SetLabelText(lbl)
        MainRps.symbol = symbol
        MainRps.youChose = True
        MainRps.choiceMsg = "2,choose," + symbol + "," + str(MainRps.score) +\
                            "," + self.rivalName  # symbol,Score,name
        msg = "2,madeAChoice" + "," + self.rivalName  # symbol,Score,name
        conn_q.put(msg)
        if MainRps.rivalChose is True:
            conn_q.put(MainRps.choiceMsg)
            MainRps.choiceMsg = ""
            MainRps.youChose = False
            MainRps.rivalChose = False

    def disable_buttons(self):  # disable buttons
        self.rock.Disable()
        self.paper.Disable()
        self.scissors.Disable()

    def enable_buttons(self):  # enable buttons
        self.rock.Enable()
        self.paper.Enable()
        self.scissors.Enable()

    def close_frame(self, event):  # player closed the frame
        msg = "close," + self.rivalName
        conn_q.put(msg)
        MainRps.score = 0
        MainRps.rScore = 0
        MainRps.round = 1
        wx.CallAfter(self.Destroy)

    def check(self):  # check who is the winner of the round
        result = ""
        if MainRps.symbol == "1":
            if MainRps.rSymbol == "2":
                MainRps.rScore = MainRps.rScore + 1
                result = self.rivalName + " wins the round"
            if MainRps.rSymbol == "3":
                MainRps.score = MainRps.score + 1
                result = "You win the round"

        if MainRps.symbol == "2":
            if MainRps.rSymbol == "3":
                MainRps.rScore = MainRps.rScore + 1
                result = self.rivalName + " win the round"
            if MainRps.rSymbol == "1":
                MainRps.score = MainRps.score + 1
                result = "You win the round"

        if MainRps.symbol == "3":
            if MainRps.rSymbol == "1":
                MainRps.rScore = MainRps.rScore + 1
                result = self.rivalName + " win the round"
            if MainRps.rSymbol == "2":
                MainRps.score = MainRps.score + 1
                result = "You win this round"
        return result

    def update(self):  # update variables after winning check
        self.bitmap1.Show()
        self.bitmap2.Show()
        if MainRps.symbol == "1":
            your_choice = wx.Image("rock.bmp", wx.BITMAP_TYPE_ANY)
        if MainRps.symbol == "2":
            your_choice = wx.Image("paper.bmp", wx.BITMAP_TYPE_ANY)
        if MainRps.symbol == "3":
            your_choice = wx.Image("scissors.bmp", wx.BITMAP_TYPE_ANY)
        your_choice = your_choice.Scale(40, 60, wx.IMAGE_QUALITY_HIGH)
        self.bitmap1.SetBitmap(wx.Bitmap(your_choice))
        if MainRps.rSymbol == "1":
            other_choice = wx.Image("rock.bmp", wx.BITMAP_TYPE_ANY)
        if MainRps.rSymbol == "2":
            other_choice = wx.Image("paper.bmp", wx.BITMAP_TYPE_ANY)
        if MainRps.rSymbol == "3":
            other_choice = wx.Image("scissors.bmp", wx.BITMAP_TYPE_ANY)
        other_choice = other_choice.Scale(40, 60, wx.IMAGE_QUALITY_HIGH)
        self.bitmap2.SetBitmap(wx.Bitmap(other_choice))
        self.msg_lbl.SetLabelText(MainRps.result)
        self.yourScore.SetLabelText(str(MainRps.score))
        self.rivalScore.SetLabelText(str(MainRps.rScore))
        self.you_lbl.SetLabelText("you chose")
        self.rival_lbl.SetLabelText("rival chose")

        sleep(3)
        self.bitmap1.Hide()
        self.bitmap2.Hide()
        self.you_lbl.SetLabelText("")
        self.rival_lbl.SetLabelText("")

        # check if one of the players won the game
        if MainRps.score == 3 or MainRps.rScore == 3:
            if MainRps.score == 3:
                self.msg_lbl.SetLabelText("You are the Winner")
                msg = "2,win"
                conn_q.put(msg)
            else:
                lbl = self.rivalName + " is the Winner"
                self.msg_lbl.SetLabelText(lbl)
        else:
            self.roundNumber.SetLabelText("ROUND " + str(MainRps.round))
            self.msg_lbl.SetLabelText("Wait for you to choose")
            self.enable_buttons()


def start(name, rival_name):
    MainRps(name, rival_name)
