import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from frames.adminwindow import *
from Controller.Controller import Controller
#table window is removed, it is obsolete
#from frames.tablewindow import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Create a tab menu, the first one is the active one when app is loaded
        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        controller = Controller()
        #table = TableView(controller)
        tabs.addTab(AdmTab(controller), "Admin")
        #tabs.addTab(table, "Products")
        self.setMinimumSize(700, 700)

        self.setCentralWidget(tabs)
