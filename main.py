import sys, time, threading

from pynput.keyboard import Controller as keyboardController, Listener as keyboardListener,  Key
from pynput.mouse import Controller as mouseController, Listener as mouseListener, Button


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QLabel, QTextBrowser, QComboBox, QListWidget, QProgressBar, QMessageBox, QDialogButtonBox, \
    QScrollBar, QScrollArea
from PyQt5 import uic
from datetime import datetime 

recording = False
macroSlot1Name = 'MacroLog1'
filehandler = 'placeholder'
mouse = mouseController()
keyboard = keyboardController()
automaticDelays = True
includeMovement = True

specialKeys = {Key.space:' '}

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

      
      if recording:
         print('flag in recording ')
         self.RecordingNotRecording.setText('recording')
         self.StopRecordingButton.setHidden(False)
      else:

         self.RecordingNotRecording.setText('not recording')
         



      self.MacroSlot1 = self.findChild(QPushButton, 'MacroSlot1')
      self.MacroSlot2 = self.findChild(QPushButton, 'MacroSlot2')
      self.MacroSlot3 = self.findChild(QPushButton, 'MacroSlot3')
      self.MacroSlot4 = self.findChild(QPushButton, 'MacroSlot4')
      self.MacroSlot5 = self.findChild(QPushButton, 'MacroSlot5')

      self.OverwriteButton = self.findChild(QPushButton, 'OverwriteButton')
      self.AddInputsButton = self.findChild(QPushButton, 'AddInputsButton')

      
      '''set event handlers '''

      self.MacroSlot1.clicked.connect(self.MacroSlot1_Clicked)
      self.UserLogScrollBar.sliderMoved.connect(self.UserLogScrollBar_Scrolled)
      self.StopRecordingButton.clicked.connect(self.StopRecordingButton_Clicked)
      self.OverwriteButton.clicked.connect(self.OverwriteButton_Clicked)
      self.AddInputsButton.clicked.connect(self.AddInputsButton_Clicked)

   def REMB_clicked(self):
      uic.loadUi('RunExistingMacro.ui', self)
      '''initialise widgets within program'''

      '''self.UserLogArea = self.findChild(QScrollArea, 'UserLogArea')
      self.UserLog = self.findChild(QLabel, 'UserLog')
      self.UserLogScrollBar = self.findChild(QScrollBar,'UserLogScrollBar')'''

      self.ViewMacroButton = self.findChild(QPushButton,'ViewButton')
      self.RunMacroButton = self.findChild(QPushButton,'RunButton')

      
      self.ViewMacroButton.setHidden(True)
      self.RunMacroButton.setHidden(True)

      self.RunMacroSlot1 = self.findChild(QPushButton, 'RunMacroSlot1')
      self.RunMacroSlot2 = self.findChild(QPushButton, 'RunMacroSlot2')
      self.RunMacroSlot3 = self.findChild(QPushButton, 'RunMacroSlot3')
      self.RunMacroSlot4 = self.findChild(QPushButton, 'RunMacroSlot4')
      self.RunMacroSlot5 = self.findChild(QPushButton, 'RunMacroSlot5')

      self.show() #display widgets

      '''set event handlers '''

      self.RunMacroSlot1.clicked.connect(self.RunMacroSlot1_Clicked)
      self.RunMacroButton.clicked.connect(self.RunMacroButton_Clicked)

      #self.UserLogScrollBar.sliderMoved.connect(self.UserLogScrollBar_Scrolled)
   def RunMacroSlot1_Clicked(self):
      print('run macro slot 1 clicked')
      global selectedMacro
      selectedMacro = 1
      self.ViewMacroButton.setHidden(False)
      self.RunMacroButton.setHidden(False)
   
   def RunMacroButton_Clicked(self):
      executor_thread.start()
      
         
   
   
   def StopRecordingButton_Clicked(self):
      global recording 
      
      self.RecordingNotRecording.setText('not recording')
      self.StopRecordingButton.setHidden(True)
      end_listeners(keyboard_listener,mouse_listener,listener_thread)
      recording = False
      
   def OverwriteButton_Clicked(self):
      f = open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog1.txt', 'w')
      f.write('\n')
      f.close()

   def AddInputsButton_Clicked(self):

      global recording 
      
      self.RecordingNotRecording.setText('recording')
      self.StopRecordingButton.setHidden(False)
      if not(recording):
         print('starting listener threads')
         listener_thread.start()
      recording = True
   
   def MacroSlot1_Clicked(self):
      
      global selectedMacro
      
      selectedMacro = macroSlot1Name
      

      
    
   def UserLogScrollBar_Scrolled(self):
      return True #placeholder value        

   
   def OSB_clicked(self): #open settings button 
      return True #placeholder return value for valid parsing 


def on_move(x,y):
   if includeMovement == True:
      f = open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog1.txt', 'a')
      f.write(f'({x},{y})\n')
      f.close()
   else:
      return True
   
def RunMacro():
   time.sleep(1)
   f = open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog1.txt', 'r')
   for line in f:
      executeMacroLine(findType(line)[0],findType(line)[1] )
   f.close()
   print('end of file reached')

def on_click(x,y,button,pressed):
   time.sleep(0.001)

   f = open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog1.txt', 'a')
   
   if button == Button.left:
      f.write(f'cl({x},{y})\n')
   elif button == Button.right:
      f.write(f'cr({x},{y})\n')
   elif button == Button.middle:
      f.write(f'cm({x},{y})\n')
   f.close()


def on_scroll(x,y,dx,dy):
   return True

def on_press(key):
   f = open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog1.txt', 'a')
   f.write(f'pressed {key}\n')
   f.close()
   
def on_release(key):
   f = open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog1.txt', 'a')
   f.write(f'released {key}\n')
   f.close()


keyboard_listener = keyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = mouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
  
def start_listeners(keyboard_listener, mouse_listener):
   

   keyboard_listener.start()
   mouse_listener.start()

   #keyboard_listener.join()
   #mouse_listener.join()

def end_listeners(keyboard_listener, mouse_listener,listener_thread):

   keyboard_listener.stop()
   mouse_listener.stop()
   

def overwrite():
   return True

def findType(line):
   isSpecialKey = False
   if line[0:2] == 'cl':
      return ['left click',None]
      
   elif line[0:2] == 'cr':
      return ['right click', None]
   
   elif line[0:2] =='m':
      return ['middle click',None ]
   elif 'Key.' in line:
      isSpecialKey = True
      return['placeholder','placeholder value ']
   
   elif line[0:3] == 'pre' and not(isSpecialKey):
      return['key',line[9]]
   elif line[0] == '(':
      commaPosition = line.find(',')
      finalBracketPosition = line.find(')')

      return['position',[line[1:commaPosition],line[commaPosition+1:finalBracketPosition]]]
   else:
      return['unknown',None]
   
def executeMacroLine(type, value):
   
   print(type, value)
   if type == 'left click':
      
      mouse.click(Button.left, 1)
      mouse.release(Button.left)

   elif type == 'right click':

      mouse.click(Button.right, 1 )
      mouse.release(Button.right)

   elif type == 'middle click':

      mouse.click(Button.middle, 1)
      mouse.release(Button.middle)
   
   elif type == 'key':
      time.sleep(0.1)
      keyboard.type(value)
   elif type == 'position':
      mouse.position = (value[0],value[1])
      
   elif type == 'unknown':
      print('unknown line type ')
   time.sleep(0.01)
   
   
   
   

   

# Run the listener in a separate thread
listener_thread = threading.Thread(target=start_listeners, daemon=True, args=(keyboard_listener,mouse_listener))
executor_thread = threading.Thread(target=RunMacro, daemon = True)
      

app = QApplication(sys.argv)
window = UI()
app.exec_()

