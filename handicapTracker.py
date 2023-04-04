import sys
import os
import calendar
import string
import ftplib
import csv

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QDateEdit, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QPlainTextEdit, QComboBox, QCalendarWidget
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from datetime import datetime
from os import path


class App(QMainWindow):
    global currentYear, currentMonth, startDate, endDate, calendarS, calendarE, startLabel, inData, dataPath, currentPath
    global primary, secondary, border, fontPrimary, fontSecondary
    inData = ""
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    
    currentPath = os.path.dirname(__file__) + "/"
    dataPath = "data.txt"
    dataPath = os.path.dirname(__file__) + "/" + dataPath
    
    primary = 'rgb(188, 235, 203)'
    secondary = 'rgb(247, 255, 246)'
    border = 'rgb(132, 145, 163)'
    fontPrimary = ''
    fontSecondary = ''
    
    try:
        f = open(dataPath, "r+")
        inData = f.read()
        f.close()
    except OSError:
        print("file not found")
        f = open(dataPath, 'w')
        f.write('Course, Score, Rating, Slope, Date\n')
        f.close()
        pass
            
    
    def __init__(self):
        super().__init__()
        self.title = 'Golf Handicap Tracker 1.0'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet('background:'+secondary+';')
        self.statusBar().showMessage('waiting for user input')
        
        #add submit button
        buttonS = QPushButton('Submit Round', self)
        buttonS.setToolTip('Add conference to database')
        buttonS.setStyleSheet('background: rgb(147, 180, 139); border-radius:10px; color:white')
        buttonS.move(60,500)
        buttonS.resize(250,50)
        buttonS.clicked.connect(self.submitRound)
        buttonS.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
       
        
        # Create the input field
        self.score = QLineEdit(self)
        self.score.setValidator(QtGui.QIntValidator(1, 999, self))
        self.score.move(20,130);
        self.score.setStyleSheet('background:'+primary+'; border-style: solid; border-width: 5px; border-color:'+border+'; border-radius:5px;')
        
        # Course Name
        self.courseBox = QLineEdit(self)
        self.courseBox.move(20, 50)
        self.courseBox.resize(320,40)
        self.courseBox.setFont(QtGui.QFont("Times", 12))
        self.courseBox.setStyleSheet('background:'+primary+'; border-style: solid; border-width: 5px; border-color:'+border+'; border-radius:5px;')
        
        # Course Rating input field
        self.rating = QLineEdit(self)
        self.rating.setValidator(QtGui.QIntValidator(1, 999, self))
        self.rating.move(130,130);
        self.rating.setStyleSheet('background:'+primary+'; border-style: solid; border-width: 5px; border-color:'+border+'; border-radius:5px;')
        
        # Slope input field
        self.slope = QLineEdit(self)
        self.slope.setValidator(QtGui.QIntValidator(1, 999, self))
        self.slope.move(240,130);
        self.slope.setStyleSheet('background:'+primary+'; border-style: solid; border-width: 5px; border-color:'+border+'; border-radius:5px;')
        
        
        self.calendarS = QCalendarWidget(self)
        self.calendarS.resize(273, 200)
        self.calendarS.move(50, 200)
        self.calendarS.setGridVisible(True)
        self.calendarS.setMinimumDate(QDate(currentYear, currentMonth - 1, 1))
        self.calendarS.setMaximumDate(QDate(currentYear, currentMonth + 1, calendar.monthrange(currentYear, currentMonth)[1]))
        self.calendarS.setSelectedDate(QDate(currentYear, currentMonth, 1))
        self.calendarS.clicked.connect(self.setStartDate)
        self.calendarS.setStyleSheet('background:'+primary+';')
        
        self.startLabel = QtWidgets.QLabel(self)
        self.startLabel.resize(270, 50)
        self.startLabel.move(50,400)
        self.startLabel.setText("select round date")
        self.startLabel.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        self.startLabel.setStyleSheet("color: rgb(2, 1, 34);")
        self.startLabel.setAlignment(QtCore.Qt.AlignCenter)
        
        
        # field labels
        titleLabel = QtWidgets.QLabel(self)
        titleLabel.move(20,15)
        titleLabel.setText("Course:")
        titleLabel.setStyleSheet('font-size:18px; color: '+fontPrimary+';');
        
        descriptionLabel = QtWidgets.QLabel(self)
        descriptionLabel.move(20,100)
        descriptionLabel.setText("Score:")
        descriptionLabel.setStyleSheet('font-size:18px; color: '+fontPrimary+';');
        
        ratingLabel = QtWidgets.QLabel(self)
        ratingLabel.move(130,100)
        ratingLabel.setText("Rating:")
        ratingLabel.setStyleSheet('font-size:18px; color: '+fontPrimary+';');
        
        ratingLabel = QtWidgets.QLabel(self)
        ratingLabel.move(130,100)
        ratingLabel.setText("Slope:")
        ratingLabel.setStyleSheet('font-size:18px; color: '+fontPrimary+';');
        
        
        # Create Table
        self.table = QTableWidget(self)
        self.table.move(400,50)
        self.table.resize(350,500)
        self.table.setStyleSheet('background:'+primary+'; font-size:15px;')
        # Load data from file
        self.loadData()
        self.show()

    def setStartDate(self):
        self.startLabel.setText(self.calendarS.selectedDate().toString('MMMM dd yyyy'))
        
    def setEndDate(self):
        self.endLabel.setText(self.calendarE.selectedDate().toString())    
        
    @pyqtSlot()
    def checkInput(self):
        print(self.calendarE.selectedDate().toString())
        
            
    def clearForm(self):
        self.courseBox.setText('') 
        self.score.setText('')

        self.calendarS.setSelectedDate(QDate(currentYear, currentMonth, 1))
        self.startLabel.setText("select start date")
        
    def submitRound(self):
        formData = self.courseBox.text() + ", "
        formData += self.score.text() + ", "
        formData += self.rating.text() + ", "
        formData += self.slope.text() + ", "
        formData += self.calendarS.selectedDate().toString('MM/dd/yyyy')
        formData += "\n"
        
        try:
            f = open(dataPath, "a+")
            f.write(formData)
            f.close()
            self.clearForm()
        except OSError:
            print("failed to write file")
            pass
            
    def loadData(self):
        try:
            with open('data.txt', newline='\n') as csvfile:
                data = csv.reader(csvfile, delimiter=',')
                header_row = next(data)  # get the header row
                # Get the number of rows in the data
                num_rows = sum(1 for row in data)    # add 1 for header row
                csvfile.seek(0)  # reset the file pointer
                # Get the number of columns in the data
                num_cols = len(header_row)
                # Set the number of rows and columns in the table
                self.table.setRowCount(num_rows)
                self.table.setColumnCount(num_cols)
                # Set the header labels
                self.table.setHorizontalHeaderLabels(header_row)
                # Add data to the table
                for row, data_row in enumerate(data, start=-1):
                    for col, item in enumerate(data_row):
                        self.table.setItem(row, col, QTableWidgetItem(item))
        except:
            print('Unable to load data') 
        
if __name__ == '__main__':
    #f.close()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())