from PyQt5 import QtWidgets
from buyerUI import Ui_Form
from addCartDialogFunction import AddCartDialog
import pymysql
import sys


class BuyerUI(QtWidgets.QWidget, Ui_Form):
    def __init__(self, db, dbcursor, Bid):
        super(BuyerUI, self).__init__()
        self.setupUi(self)

        self.db = db
        self.dbcursor = dbcursor
        self.Bid = Bid
        self.page = 1

        self.commodityTableWidget.setColumnWidth(0, 40)
        self.commodityTableWidget.setColumnWidth(1, 80)
        self.commodityTableWidget.setColumnWidth(2, 150)
        self.commodityTableWidget.setColumnWidth(3, 60)
        self.commodityTableWidget.setColumnWidth(4, 60)

        self.getAllData()

        self.initTable()

        self.commodityPageLabel.setText(str(self.page))
        self.enablePagePushButton()
        self.reShow()

        self.commoditySearchPushButton.clicked.connect(self.searchCommodity)
        self.addCartPushButton.clicked.connect(self.addCart)

    def searchCommodity(self):
        self.sql = 'select Cname, Cdescribe, commodity.stockSize, price, discount, commodity.Cid, stock, address ' \
                   'from commodity, warehouse ' \
                   'where commodity.Cid = warehouse.stockCid and commodity.stockSize = warehouse.stockSize ' \
                   'and Cname like \"%' + self.commoditySearchLineEdit.text() + '%\";'
        self.dbcursor.execute(self.sql)
        self.data = self.dbcursor.fetchall()
        self.page = 1
        self.reShow()

    def addCart(self):
        for i in range(0, 3):
            if i == 0:
                self.addCartDialog = AddCartDialog(self.db, self.dbcursor, self.Bid,
                                                   self.data[self.page * 3 - 3 + i][5],
                                                   self.data[self.page * 3 - 3 + i][0],
                                                   self.data[self.page * 3 - 3 + i][2],
                                                   self.data[self.page * 3 - 3 + i][6])
                self.addCartDialog.show()


    def initTable(self):
        if self.page * 3 - 3 + 0 < len(self.data):
            self.widget1 = QtWidgets.QWidget()
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget1)
            spacerItem1 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem1)
            self.checkBox1 = QtWidgets.QCheckBox(self.widget1)
            self.horizontalLayout.addWidget(self.checkBox1)
            spacerItem2 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem2)
            self.commodityTableWidget.setCellWidget(0, 0, self.widget1)
            self.textBrowser1 = QtWidgets.QTextBrowser()
            self.commodityTableWidget.setCellWidget(0, 2, self.textBrowser1)

        if self.page * 3 - 3 + 1 < len(self.data):
            self.widget2 = QtWidgets.QWidget()
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget2)
            spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem3)
            self.checkBox2 = QtWidgets.QCheckBox(self.widget2)
            self.horizontalLayout.addWidget(self.checkBox2)
            spacerItem4 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem4)
            self.commodityTableWidget.setCellWidget(1, 0, self.widget2)
            self.textBrowser2 = QtWidgets.QTextBrowser()
            self.commodityTableWidget.setCellWidget(1, 2, self.textBrowser2)

        if self.page * 3 - 3 + 2 < len(self.data):
            self.widget3 = QtWidgets.QWidget()
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget3)
            spacerItem5 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem5)
            self.checkBox3 = QtWidgets.QCheckBox(self.widget3)
            self.horizontalLayout.addWidget(self.checkBox3)
            spacerItem6 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.horizontalLayout.addItem(spacerItem6)
            self.commodityTableWidget.setCellWidget(2, 0, self.widget3)
            self.textBrowser3 = QtWidgets.QTextBrowser()
            self.commodityTableWidget.setCellWidget(2, 2, self.textBrowser3)

        self.checkBox1.stateChanged.connect(self.enableFuncPushButton)
        self.checkBox2.stateChanged.connect(self.enableFuncPushButton)
        self.checkBox3.stateChanged.connect(self.enableFuncPushButton)

    def enablePagePushButton(self):
        if self.page == 1:
            self.commodityLastPushButton.setEnabled(False)
        else:
            self.commodityLastPushButton.setEnabled(True)

        if self.page * 3 >= len(self.data):
            self.commodityNextPushButton.setEnabled(False)
        else:
            self.commodityNextPushButton.setEnabled(True)

    def enableFuncPushButton(self):
        if self.checkBox1.isChecked() or self.checkBox2.isChecked() or self.checkBox3.isChecked():
            self.addCartPushButton.setEnabled(True)
        else:
            self.addCartPushButton.setEnabled(False)

    def getAllData(self):
        self.sql = 'select Cname, Cdescribe, commodity.stockSize, price, discount, commodity.Cid, stock, address ' \
                   'from commodity, warehouse ' \
                   'where commodity.Cid = warehouse.stockCid and commodity.stockSize = warehouse.stockSize;'
        self.dbcursor.execute(self.sql)
        self.data = self.dbcursor.fetchall()

    def showData(self):
        self.clearTable()
        for i in range(0, 3):
            if self.page * 3 - 3 + i < len(self.data):
                for j in [1, 3]:
                    self.commodityTableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(
                        str(self.data[self.page * 3 - 3 + i][j - 1])))
                if i == 0:
                    self.textBrowser1.setText(self.data[self.page * 3 - 3 + i][1])
                    self.commodityTableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(
                        str(self.data[self.page * 3 - 3 + i][3] * self.data[self.page * 3 - 3 + i][4])))
                elif i == 1:
                    self.textBrowser2.setText(self.data[self.page * 3 - 3 + i][1])
                    self.commodityTableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(
                        str(self.data[self.page * 3 - 3 + i][3] * self.data[self.page * 3 - 3 + i][4])))
                elif i == 2:
                    self.textBrowser3.setText(self.data[self.page * 3 - 3 + i][1])
                    self.commodityTableWidget.setItem(i, 4, QtWidgets.QTableWidgetItem(
                        str(self.data[self.page * 3 - 3 + i][3] * self.data[self.page * 3 - 3 + i][4])))
            else:
                break

    def showPage(self):
        self.commodityPageLabel.setText('第' + str(self.page) + '页')

    def reShow(self):
        self.showData()
        self.enableFuncPushButton()
        self.showPage()

    def clearCheckBox(self):
        self.checkBox1.setCheckState(False)
        self.checkBox2.setCheckState(False)
        self.checkBox3.setCheckState(False)

    def clearTable(self):
        self.commodityTableWidget.clearContents()
        self.initTable()


if __name__ == "__main__":
    db = pymysql.connect("localhost", "root", "130e340", "e-commerce")
    cursor = db.cursor()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    buyerUI = BuyerUI(db, cursor, "001")
    buyerUI.show()
    sys.exit(app.exec_())