from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from GUI import Ui_MainWindow
import sys
from Sudoku_generator import generate, checking


class mainwindow(QtWidgets.QMainWindow):
    """Главное окно интерфейса"""
    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.newgame)
        self.ui.pushButton_2.clicked.connect(self.check)
        self.ui.pushButton_3.clicked.connect(self.cancelcheck)
        self.ui.pushButton_3.setHidden(True)
        self.setWindowTitle("Судоку")
    def check(self):
        """Проверяет верность заполнения таблицы
        Если верно, выводит надпись 'Верно', иначе - 'Неверно' и подсвечивает элемент, в котором ошибка """
        gr = []
        s = self.ui.tableWidget.rowCount()
        for i in range(s):
            gr.append([])
            for j in range(s):
                gr[i].append(self.ui.tableWidget.item(i, j).text())
        for i in range(s):
            for j in range(s):
                try:
                    gr[i][j] = int(gr[i][j])
                except:
                    gr[i][j] = None
                if gr[i][j] != None and (gr[i][j] > s or gr[i][j] <=0):
                    gr[i][j] = None
        c = checking(gr)
        if c == True:
            self.ui.label_3.setText('Верно')
        else:
            self.ui.label_3.setText('Неверно')
            if c[2] == 3:
                self.ui.tableWidget.item(c[0], c[1]).setBackground(QtGui.QColor(192, 240, 192))
                self.ui.label_3.setText('Неполное \nрешение')
            elif c[2] == 0:
                for i in range(s):
                    self.ui.tableWidget.item(i, c[1]).setBackground(QtGui.QColor(240, 192, 192))
            elif c[2] == 1:
                for i in range(s):
                    self.ui.tableWidget.item(c[0], i).setBackground(QtGui.QColor(240, 192, 192))
            elif c[2] == 2:
                s = int(s**0.5)
                for i in range(s*c[0], s*c[0]+s):
                    for j in range(s*c[1],s*c[1]+s):
                        self.ui.tableWidget.item(i, j).setBackground(QtGui.QColor(240, 192, 192))
            self.ui.pushButton_3.setVisible(True)

    def cancelcheck(self):
        """Возвращает интерфейс в начальное состояние после отмены проверки"""
        self.coloring()
        self.ui.pushButton_3.setHidden(True)
        self.ui.label_3.setText('')

    def setdif(self):
        """Получает значение сложности"""
        diff = self.ui.comboBox.currentIndex()
        return diff

    def setsize(self):
        """Получает значение размера"""
        if self.ui.comboBox_2.currentIndex() == 0:
            s = 3
        else:
            s = 4
        return s

    def coloring(self):
        """Раскрашивает таблицу в шахматном порядке в голубой и белый цвета"""
        size = int(self.ui.tableWidget.rowCount()**0.5)
        for i in range(self.ui.tableWidget.rowCount()):
            for j in range(self.ui.tableWidget.rowCount()):
                if (i // size + j // size) % 2 == 0:
                    self.ui.tableWidget.item(i, j).setBackground(QtGui.QColor(240, 240, 255))
                else:
                    self.ui.tableWidget.item(i, j).setBackground(QtGui.QColor(255, 255, 255))


    def newgame(self):
        """Начинает новую игру"""
        size = self.setsize()
        difficulty = self.setdif()
        self.ui.label_3.setText('')
        sudoku = generate(size, difficulty)
        self.ui.tableWidget.setColumnCount(size**2)
        self.ui.tableWidget.setRowCount(size**2)
        if size == 3:
            self.resize(854, 633)
            self.ui.tableWidget.setGeometry(QtCore.QRect(240, 10, 576, 576))
            for i in range(size**2):
                self.ui.tableWidget.setColumnWidth(i, 576 // size**2)
                self.ui.tableWidget.setRowHeight(i, 576 // size**2)
        else:
            self.resize(1300, 950)
            self.ui.tableWidget.setGeometry(QtCore.QRect(240, 10, 992, 896))
            for i in range(size**2):
                self.ui.tableWidget.setColumnWidth(i, 992 // size**2)
                self.ui.tableWidget.setRowHeight(i, 896 // size**2)
        for i in range(size**2):
            for j in range(size**2):
                if sudoku[i][j] != 0:
                    cellinfo = QTableWidgetItem(str(sudoku[i][j]))
                    cellinfo.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.ui.tableWidget.setItem(i, j, cellinfo)
                    self.ui.tableWidget.item(i, j).setForeground(QtGui.QColor(0, 0, 100))
                else:
                    cellinfo = QTableWidgetItem(' ')
                    self.ui.tableWidget.setItem(i, j, cellinfo)
        self.coloring()


app = QtWidgets.QApplication([])
application = mainwindow()
application.show()

sys.exit(app.exec())
