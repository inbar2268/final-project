class Users:
    def __init__(self, conn, tablename="users", username="username",
                 password="password", name="name", online="online",
                 play="play"):
        self.__tablename = tablename
        self.__password = password
        self.__username = username
        self.__name = name
        self.__online = online  # 1=online 0=offline
        self.__play = play  # 1=in a game 0=not in a game
        self.conn = conn
        # create table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS USERS
                    (
                    username	TEXT    NOT NULL,
                    password    TEXT	NOT NULL,
                    name    TEXT    NOT NULL,
                    online    CHAR    NOT NULL,
                    play    CHAR    NOT NULL
                    );''')

        self.conn.commit()

    # insert new user to data base
    def insert_user(self, username, password, name):
        str_insert = "INSERT INTO " + self.__tablename + " (" + \
                     self.__username + "," + self.__password + "," + \
                     self.__name + "," + self.__online + "," + self.__play + \
                     ") VALUES (" + "'" + username + "'" + "," + "'" + \
                     password + "'" + "," + "'" + name + "'" + "," + "'" \
                     + '0' + "'" + "," + "'" + '0' + "'" + ");"
        self.conn.execute(str_insert)
        self.conn.commit()  # save the changes

    def update_online(self, name, online):
        # insert online data
        self.conn.execute("UPDATE users SET online = (?) WHERE name = (?)",
                          (online, name))
        self.conn.commit()

    def update_play(self, name, play):
        self.conn.execute("UPDATE users SET play = (?) WHERE name = (?)",
                          (play, name))
        self.conn.commit()


class Wins:
    def __init__(self, conn, tablename="wins", name="name",
                 tic_tac_toe="tic_tac_toe",
                 rock_paper_scissors="rock_paper_scissors"):
        self.__tablename = tablename
        self.__name = name
        self.__tic_tac_toe = tic_tac_toe
        self.__rock_paper_scissors = rock_paper_scissors
        self.conn = conn
        # create table
        self.conn.execute('''CREATE TABLE IF NOT EXISTS WINS
                    (
                    name    TEXT    NOT NULL,
                    tic_tac_toe    TEXT    NOT NULL,
                    rock_paper_scissors    TEXT    NOT NULL
                    );''')

        self.conn.commit()

    # insert new player to data base
    def insert_player(self, name):
        str_insert = "INSERT INTO " + self.__tablename + " (" + self.__name +\
                     "," + self.__tic_tac_toe + "," + \
                     self.__rock_paper_scissors + ") VALUES (" + "'" + name + \
                     "'" + "," + "'" + '0' + "'" + "," + "'" + '0' + "'" + ");"
        self.conn.execute(str_insert)
        self.conn.commit()  # save the changes

    # insert an updated amount of wins
    def update_tic_tac_toe(self, name, win):
        self.conn.execute("UPDATE wins SET tic_tac_toe = (?) WHERE name = (?)",
                          (win, name))
        self.conn.commit()
        print("update_tic_tac_toe")

    # insert an updated amount of wins
    def update_rock_paper_scissors(self, name, win):
        self.conn.execute("UPDATE wins SET rock_paper_scissors = (?)"
                          " WHERE name = (?)",
                          (win, name))
        self.conn.commit()
        print("update")
