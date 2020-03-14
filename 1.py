import sys
import pymysql.cursors
from vishlist import *
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QMessageBox, QCheckBox, QPushButton
from PyQt5.QtCore import QCoreApplication, Qt


connect = pymysql.connect(host='localhost', user='root', password='Kurama1111111111', db='vishlist', charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)

with connect.cursor() as cursor:
    cursor.execute("""SELECT some_text 
    FROM vishlist.some_table""")
    _list = cursor.fetchall()


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setRowCount(len(_list))
        self.len_list = len(_list)
        self.fill()
        self.ui.pushButton.clicked.connect(self.btnClicked)
        self.ui.pushButton_2.clicked.connect(self.btnClicked_2)
        self.OldRow = -1
        self.ui.tableWidget.clicked.connect(self.tableClicked)
        self.show()

    def tableClicked(self):
        if self.OldRow != -1:
            self.ui.tableWidget.removeCellWidget(self.OldRow, 0)
        row = self.ui.tableWidget.currentRow()
        button = QPushButton('Delete')
        self.ui.tableWidget.setCellWidget(row, 0, button)
        self.OldRow = row
        button.clicked.connect(self.btnClicked_3)




    def btnClicked(self):

        row = self.ui.tableWidget.currentRow()
        col = self.ui.tableWidget.currentColumn()
        value = self.ui.tableWidget.item(row, col).text()
        with connect.cursor() as cursor:
            cursor.execute("""UPDATE some_table
            SET some_text = '%(value)s'
            WHERE id = %(row)s""" % {'value': value, 'row': row+1})
            connect.commit()

    def btnClicked_2(self):
        self.ui.tableWidget.insertRow(self.len_list)
        with connect.cursor() as cursor:
            cursor.execute("""INSERT INTO some_table (id)
            VALUES (%(row)s)""" % {'row': self.len_list+1})
            connect.commit()
            check = QCheckBox()
            self.ui.tableWidget.setCellWidget(self.len_list, 2, check)
            self.len_list += 1
            check.clicked.connect(self.checkKlicked)

    def btnClicked_3(self):
        row = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(row)
        with connect.cursor() as cursor:
            cursor.execute("""DELETE FROM vishlist.some_table
            WHERE ID = %(row)s;""" % {'row': row+1})
            connect.commit()
            cursor.execute("SET @i :=0")
            cursor.execute("UPDATE some_table SET  id = (@i:= @i + 1)")
            cursor.execute("ALTER TABLE some_table AUTO_INCREMENT = 1;")
            connect.commit()

        self.OldRow = -1
        self.len_list -= 1

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Предупреждение',
                                     "Вы уверены, что хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            connect.close()
            event.accept()
        else:
            event.ignore()

    def fill(self):

        identifier = 0
        while identifier <= len(_list)-1:
            with connect.cursor() as cursor:
                cursor.execute("""SELECT some_text 
                FROM vishlist.some_table
                WHERE id = %(identifier)s""" % {'identifier': identifier+1})
                result = cursor.fetchone()
            self.ui.tableWidget.setItem(identifier, 1, QTableWidgetItem(result['some_text']))
            check = QCheckBox()
            self.ui.tableWidget.setCellWidget(identifier, 2, check)
            with connect.cursor() as cursor:
                cursor.execute("""SELECT checkBox
                FROM vishlist.some_table
                WHERE id = %(identifier)s""" % {'identifier': identifier+1})
                result_2 = cursor.fetchone()
                if result_2['checkBox'] == 1:
                    check.setChecked(True)
            identifier += 1
            check.stateChanged.connect(self.checkKlicked)

    def checkKlicked(self, state):
        row = self.ui.tableWidget.currentRow()
        if state == Qt.Checked:
            with connect.cursor() as cursor:
                cursor.execute("""UPDATE some_table
                SET checkBox = 1
                WHERE id = %(row)s""" % {'row': row + 1})
                connect.commit()
        else:
            with connect.cursor() as cursor:
                cursor.execute("""UPDATE some_table
                SET checkBox = 0
                WHERE id = %(row)s""" % {'row': row + 1})
                connect.commit()


# create ="""create database vishlist;
#         use vishlist;
#         CREATE TABLE some_table( `id` INT NOT NULL AUTO_INCREMENT,
#         `some_text` VARCHAR (255) NULL, PRIMARY KEY (`id`));"""
# for element in create.split(';'):
#     try:
#         print(element)
#         connection.cursor().execute(element)
#         connection.commit()
#     except:
#         print ("FALL IN " + str(element))
# connection.close()

# prim = input('Введите значение: ')
# connect = pymysql.connect(host='localhost', user='root', password='Kurama1111111111', db='vishlist', charset='utf8mb4',
#                           cursorclass=pymysql.cursors.DictCursor)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWin()
    w.setWindowTitle('Вишлист')
    sys.exit(app.exec_())


