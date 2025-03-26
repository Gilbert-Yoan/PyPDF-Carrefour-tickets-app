import sqlite3
import os

#Defaults to product.db
class Session():


    def __init__(self, master, db):
        self.db = db
        self.Controller = master
        self.con = None
        self.curs = None

    #Starts session with product.db at the root level
    def start_session(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        parent_path = os.path.abspath(os.path.join(parent_path, os.pardir))
        db_path = parent_path +  "\\" + self.db

        self.con = sqlite3.connect(db_path)
        self.curs = self.con.cursor()
        return self.con, self.curs

    #Connector is required to end the session
    def end_session(self, con):
        self.con.commit()
        self.con.close()
