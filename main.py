import sys, time

from pynput.mouse import Controller, Listener
from pynput.keyboard import Controller, Listener, Key, KeyCode

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QLabel, QTextBrowser, QComboBox, QListWidget, QProgressBar, QMessageBox, QDialogButtonBox, \
    QScrollBar, QScrollArea
from PyQt5 import uic
from datetime import datetime

recording = False

class UI(QMainWindow):

    def __init__(self):

        super(UI,self).__init__()

        uic.loadUi('MainMenu.ui', self)

        '''initialise widgets in program'''

        self.CreateNewMacroButton = self.findChild(QPushButton, 'CreateNewMacro')
        self.RunExistingMacroButton = self.findChild(QPushButton,'RunExistingMacro')
        self.OpenSettingsButton = self.findChild(QPushButton,'OpenSettings')
        
      

        self.BackgroundImage = self.findChild(QLabel,'BackgroundImage')
        self.show() #display widgets 


        '''set event handlers '''

        self.CreateNewMacroButton.clicked.connect(self.CNMB_clicked) #CNMB here is an abbreviation
        self.RunExistingMacroButton.clicked.connect(self.REMB_clicked)
        self.OpenSettingsButton.clicked.connect(self.OSB_clicked)
       
        

    '''define events '''

    def CNMB_clicked(self):
         uic.loadUi('CreateNewMacro.ui', self)

         '''initialise widgets within program'''
         self.UserLogArea = self.findChild(QScrollArea, 'UserLogArea')
         self.UserLog = self.findChild(QLabel, 'UserLog')
         self.UserLogScrollBar = self.findChild(QScrollBar,'UserLogScrollBar')

         self.RecordingNotRecording = self.findChild(QLabel,'RecordingNotRecording')
         self.StopRecordingButton = self.findChild(QPushButton,'StopRecordingButton')
         self.StopRecordingButton.setHidden(True)


         if recording == True:
            self.RecordingNotRecording.setText('recording')
            self.StopRecordingButton.setHidden(False)
         else:
            self.RecordingNotRecording.setText('not recording')



         self.MacroSlot1 = self.findChild(QPushButton, 'MacroSlot1')
         self.MacroSlot2 = self.findChild(QPushButton, 'MacroSlot2')
         self.MacroSlot3 = self.findChild(QPushButton, 'MacroSlot3')
         self.MacroSlot4 = self.findChild(QPushButton, 'MacroSlot4')
         self.MacroSlot5 = self.findChild(QPushButton, 'MacroSlot5')

         self.show() # display widgets 

         '''set event handlers '''

         self.MacroSlot1.clicked.connect(self.MacroSlot1_Clicked)
         self.UserLogScrollBar.sliderMoved.connect(self.UserLogScrollBar_Scrolled)


    def MacroSlot1_Clicked(self):
       print(self.UserLog.text())
       for i in range (50):
        self.UserLog.setText(f'{str(self.UserLog.text())} MacroSlot1 Clicked!{str(i)}\n')
    
    def UserLogScrollBar_Scrolled(self):
       return True #placeholder value        
    
    def REMB_clicked(self): #run existing macro button
       return True #placeholder return value for valid parsing 

        
    def OSB_clicked(self): #open settings button 
      return True #placeholder return value for valid parsing 


app = QApplication(sys.argv)
window = UI()
app.exec_()







sys.exit(app.exec_())
