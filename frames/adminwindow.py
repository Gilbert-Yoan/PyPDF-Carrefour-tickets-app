import sys
import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *


class AdmTab(QMainWindow):


    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.label = QLabel("Administration Panel")
        self.setWindowTitle("Receipt dataviz")

        #Declaring all buttons and their behavior
        init_db_button = QPushButton("Create database")
        init_db_button.clicked.connect(self.exec_init_db)
        all_files_button = QPushButton("Add all tickets to database")
        all_files_button.clicked.connect(self.exec_all_files)
        empty_no_restore_button = QPushButton("Empty database without restoring")
        empty_no_restore_button.clicked.connect(self.exec_empty_no_restore)
        empty_restore_button = QPushButton("Empty database and restore tickets")
        empty_restore_button.clicked.connect(self.exec_empty_restore)

        #Trying to get number of items in DB if available, same for recent date
        try :
            self.data_desc = QLabel("Number of products in DB : {}".format(self.controller.loader.get_products()))
            self.recent_date = QLabel("Most recent ticket in DB : {}".format(self.controller.loader.get_recent_date()))
            init_db_button.hide()
        except Exception as e:
            print(e)
            self.data_desc = QLabel("DATABASE AND TABLES MAY NOT EXIST")
            self.recent_date = QLabel("")
            init_db_button.show()



        layout = QGridLayout()
        #Object,row then column
        layout.addWidget(self.label, 0, 1)
        layout.addWidget(self.data_desc, 1, 0)
        layout.addWidget(self.recent_date, 2, 0)
        layout.addWidget(init_db_button, 3, 0)
        layout.addWidget(all_files_button, 2, 2)
        layout.addWidget(empty_no_restore_button, 3, 2)
        layout.addWidget(empty_restore_button, 4, 2)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    """Initiates database and tables"""
    def exec_init_db(self):
        print("Create database!")
        self.controller.initializer.sql_init()
        os.execl(sys.executable, sys.executable, *sys.argv)

    #Gets all files in the source_receipts folders and feeds them to OCR before inserting into DB.
    def exec_all_files(self):
        print("Add all files!")
        self.controller.reader.ingest_files()
        os.execl(sys.executable, sys.executable, *sys.argv)

    #Empties DB but leaves the files in the archived_receipts folder
    def exec_empty_no_restore(self):
        print("Empty without restoring!")
        self.controller.initializer.truncate_all()
        os.execl(sys.executable, sys.executable, *sys.argv)

    #Empties DB and moves files from archived_receipts to source_receipts folder
    def exec_empty_restore(self):
        print("Empty and restore!")
        self.controller.filesystem.restore_files()
        self.controller.initializer.truncate_all()
        os.execl(sys.executable, sys.executable, *sys.argv)
