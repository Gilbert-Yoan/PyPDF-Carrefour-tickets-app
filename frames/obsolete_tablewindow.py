import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

""" This is a QTableView and a TableModel to change descriptions of items

Most of this has been copied from online forums
Solid base found at the following URL
https://www.pythonguis.com/faq/editing-pyqt-tableview/
"""

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, controller):
        super(TableModel, self).__init__()
        self.controller = controller
        try :
            self._data = self.controller.loader.sql_load_desc(True)
        except Exception as e:
            self.controller.initializer.sql_init()
            self._data = self.controller.loader.sql_load_desc(True)


        self.hheaders = ['ID', 'Name', 'Description', 'Tax category','Check','Quantity']

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        if len(self._data) != 0:
            return len(self._data[0])
        else:
            return 0

    def data(self, index, role=Qt.DisplayRole):
        value = ''
        if index.isValid():
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]
                return str(value)

    """Call the controller to update in database
    Also controlling if column is 2 (description) before updating"""
    def setData(self, index, value, role):
        if role == Qt.EditRole and index.column() in (2,4,5) :
            self._data[index.row()][index.column()] = value
            if index.column() == 2 :
                self.controller.editer.update_desc(self._data[index.row()][0], value)
            return True
        return False

    """Sets flags to enable editing"""
    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable

    """May actually be optimizable
    Sets column headers
    """
    def headerData(self, section, orientation, role):
        # row and column headers
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.hheaders[section]
        return QtCore.QVariant()

    """Updates data when button clicked"""
    def update_data(self, isnull, txt=""):
        self._data = self.controller.loader.sql_load_desc(isnull, txt)


"""Creates the TableView and maps the model to it"""
class TableView(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.table = QtWidgets.QTableView()
        self.model = TableModel(controller)

        self.table.setModel(self.model)

        self.show_null = QCheckBox("Show all")
        self.show_null.setChecked(True)
        self.show_null.stateChanged.connect(self.filterchange)

        self.input = QLineEdit()
        self.input.textChanged.connect(self.filterchange)

        refresh_button = QPushButton("Refresh price")
        refresh_button.clicked.connect(self.refresh_price)
        predict_button = QPushButton("Create prediction")
        predict_button.clicked.connect(self.create_prediction)
        self.price = QLabel("Price : 0.00€")

        self.label = QLabel("Description editing ! (also lists all your products)")
        self.setWindowTitle("Receipt dataviz - Change desc")

        input_label = QLabel("Filter here :")


        main_layout = QGridLayout()
        #QVBoxLayout is first insert == at the top
        input_layout = QVBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.input)
        input_layout.addWidget(self.show_null)
        input_layout.addWidget(refresh_button)
        input_layout.addWidget(predict_button)
        input_layout.addWidget(self.price)
        input_layout.addStretch() #Helps to reduce padding

        #Object,row then column
        main_layout.addWidget(self.label, 0, 0)
        main_layout.addWidget(self.table, 1, 0)
        main_layout.addLayout(input_layout, 1, 1)
        main_layout.setColumnStretch(0, 5)
        main_layout.setRowStretch(1, 5) #Stretch needed for col or row spanning

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    """Updates model's data and refreshes the QTableView"""
    def filterchange(self):
        self.model.update_data(self.show_null.isChecked(), self.input.text())
        self.table.viewport().update()

    def refresh_price(self):
        price = 0
        for x in self.model._data :
            if x[4] == '1':
                #Here we query database for the most recent price of the item
                price = price + (self.model.controller.loader.get_recent_price(x[0]) * float(x[5]))
        self.price.setText("Price : " + str(price) + "€")

    def create_prediction(self):
        self.model.controller.inserter.insert_prediction(self.model._data)
        print("predict")
