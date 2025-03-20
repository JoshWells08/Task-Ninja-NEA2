import sys, time, threading, csv, os

from pynput.keyboard import Controller as keyboardController, Listener as keyboardListener,  Key
from pynput.mouse import Controller as mouseController, Listener as mouseListener, Button


from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, \
    QLabel, QTextBrowser, QComboBox, QListWidget, QProgressBar, QMessageBox, QDialogButtonBox, \
    QScrollBar, QScrollArea, QLineEdit, QCheckBox, QDial
from PyQt5 import uic
from datetime import datetime 

recording = False
filehandler = 'placeholder'
mouse = mouseController()
keyboard = keyboardController()
includeMovement = True
setDelays = False
setDelayValue = 0
oldtime= time.time()
skipnext = False
HotKeyPressed = False
hotkey = 'h'
timesToRunNum = 1
limitedRunTimes = True

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
         
         self.RecordingNotRecording.setText('recording')
         self.StopRecordingButton.setHidden(False)
      else:

         self.RecordingNotRecording.setText('not recording')
         



      self.MacroSlot1 = self.findChild(QPushButton, 'MacroSlot1')
      self.MacroSlot2 = self.findChild(QPushButton, 'MacroSlot2')
      self.MacroSlot3 = self.findChild(QPushButton, 'MacroSlot3')
      self.MacroSlot4 = self.findChild(QPushButton, 'MacroSlot4')
      self.MacroSlot5 = self.findChild(QPushButton, 'MacroSlot5')
      
      rows =[]
      
      with open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\filenames.csv', 'r') as csvfile:
         csvreader = csv.reader(csvfile)
         for row in csvreader:
            if not(row==[]):
               rows.append(row)

      self.MacroSlot1.setText(rows[1][1])
      self.MacroSlot2.setText(rows[2][1])
      self.MacroSlot3.setText(rows[3][1])
      self.MacroSlot4.setText(rows[4][1])
      self.MacroSlot5.setText(rows[5][1])

      self.RenameButton = self.findChild(QPushButton, 'ChangeNameButton')
      self.OverwriteButton = self.findChild(QPushButton, 'OverwriteButton')
      self.AddInputsButton = self.findChild(QPushButton, 'AddInputsButton')

      self.SelectedMacroLabel = self.findChild(QLabel, 'MacroSelectedLabel')
      self.SelectedMacroLabel.setHidden(True)

      self.ReturnButton1 = self.findChild(QPushButton, 'MenuReturn1')
      
      '''set event handlers '''

      self.MacroSlot1.clicked.connect(lambda: self.CreateMacroSlot_Clicked(1))
      self.MacroSlot2.clicked.connect(lambda: self.CreateMacroSlot_Clicked(2))
      self.MacroSlot3.clicked.connect(lambda: self.CreateMacroSlot_Clicked(3))
      self.MacroSlot4.clicked.connect(lambda: self.CreateMacroSlot_Clicked(4))
      self.MacroSlot5.clicked.connect(lambda: self.CreateMacroSlot_Clicked(5))

      self.UserLogScrollBar.sliderMoved.connect(self.UserLogScrollBar_Scrolled)
      self.RenameButton.clicked.connect(self.RenameButton_Clicked)
      self.StopRecordingButton.clicked.connect(self.StopRecordingButton_Clicked)
      self.OverwriteButton.clicked.connect(self.OverwriteButton_Clicked)
      self.AddInputsButton.clicked.connect(self.AddInputsButton_Clicked)

      self.RenameLineEdit = self.findChild(QLineEdit,'NewNameLineEdit')
      self.RenameEnter = self.findChild(QPushButton, 'NewNameEnter')

      self.RenameEnter.clicked.connect(self.RenameEnter_Clicked)

      self.RenameLineEdit.setHidden(True)
      self.RenameEnter.setHidden(True)



   def CreateMacroSlot_Clicked(self, SlotNumber):

      i=0
      MacroSlotName = ''
      global selectedMacro
      global selectedMacroPosition

      
      self.SelectedMacroLabel.setText(f'{SlotNumber}')
      self.SelectedMacroLabel.setHidden(False)
      selectedMacro = MacroSlotName
      selectedMacroPosition = SlotNumber

   def REMB_clicked(self):
      uic.loadUi('RunExistingMacro.ui', self)
      '''initialise widgets within program'''

      '''self.UserLogArea = self.findChild(QScrollArea, 'UserLogArea')
      self.UserLog = self.findChild(QLabel, 'UserLog')
      self.UserLogScrollBar = self.findChild(QScrollBar,'UserLogScrollBar')'''

      
      self.RunMacroButton = self.findChild(QPushButton,'RunButton')

      
      
      self.RunMacroButton.setHidden(True)

      self.RunMacroSlot1 = self.findChild(QPushButton, 'RunMacroSlot1')
      self.RunMacroSlot2 = self.findChild(QPushButton, 'RunMacroSlot2')
      self.RunMacroSlot3 = self.findChild(QPushButton, 'RunMacroSlot3')
      self.RunMacroSlot4 = self.findChild(QPushButton, 'RunMacroSlot4')
      self.RunMacroSlot5 = self.findChild(QPushButton, 'RunMacroSlot5')

      self.SelectedMacroLabel = self.findChild(QLabel, 'MacroSelectedLabel')
      self.SelectedMacroLabel.setHidden(True)

      rows =[]
      
      with open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\filenames.csv', 'r') as csvfile:
         csvreader = csv.reader(csvfile)
         for row in csvreader:
            if not(row==[]):
               rows.append(row)

      self.RunMacroSlot1.setText(rows[1][1])
      self.RunMacroSlot2.setText(rows[2][1])
      self.RunMacroSlot3.setText(rows[3][1])
      self.RunMacroSlot4.setText(rows[4][1])
      self.RunMacroSlot5.setText(rows[5][1])

      self.timesToRun = self.findChild(QLineEdit,'timesToRun')
      self.runUntilStoppedBox = self.findChild(QCheckBox,'runUntilStoppedBox')

      self.speedDial = self.findChild(QSpe)

      self.show() #display widgets

      '''set event handlers '''

      self.RunMacroSlot1.clicked.connect(lambda: self.RunMacroSlot_Clicked(1))
      self.RunMacroSlot2.clicked.connect(lambda: self.RunMacroSlot_Clicked(2))
      self.RunMacroSlot3.clicked.connect(lambda: self.RunMacroSlot_Clicked(3))
      self.RunMacroSlot4.clicked.connect(lambda: self.RunMacroSlot_Clicked(4))
      self.RunMacroSlot5.clicked.connect(lambda: self.RunMacroSlot_Clicked(5))

      self.RunMacroButton.clicked.connect(self.RunMacro)

      #self.UserLogScrollBar.sliderMoved.connect(self.UserLogScrollBar_Scrolled)

   def RunMacro(self):
      global HotKeyPressed
      try:
         timesToRunNum = int(self.timesToRun.text()) 
         #print(timesToRunNum,'odskfkdko')
      except ValueError:
         print('value error ')
      
      limitedRunTimes = not(self.runUntilStoppedBox.checkState())
      
      time.sleep(1)
      f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'r')
      if limitedRunTimes:
         for i in range(0,timesToRunNum,1): 
            if not(HotKeyPressed):
               f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'r')
               for line in f:
                  if setDelays:
                     time.sleep(setDelayValue)
                  if not HotKeyPressed:
                     executeMacroLine(findType(line)[0],findType(line)[1] )
               f.close()      
      else: 
         while not HotKeyPressed:
            f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'r')
            for line in f:
               if not HotKeyPressed:
                  if setDelays:
                     time.sleep(setDelayValue)
                  if not HotKeyPressed:
                     executeMacroLine(findType(line)[0],findType(line)[1] )
            f.close()
      HotKeyPressed = False
   
      
   def RunMacroSlot_Clicked(self, SlotNumber):

      rows =[]
      
      with open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\filenames.csv', 'r') as csvfile:
         csvreader = csv.reader(csvfile)
         for row in csvreader:
            if not(row==[]):
               rows.append(row)
      
      
      global selectedMacro
      global selectedMacroPosition

      selectedMacro = rows[SlotNumber][1]
      selectedMacroPosition = SlotNumber
      
      
      self.SelectedMacroLabel.setText(f'{SlotNumber}')
      self.SelectedMacroLabel.setHidden(False)
      
      
      
      self.RunMacroButton.setHidden(False)


   
   def RunMacroButton_Clicked(self):
      global timesToRunNum
      try:
         timesToRunNum = int(self.timesToRun.text()) 
         #print(timesToRunNum,'odskfkdko')
      except ValueError:
         print('value error ')
      
   
   def RenameButton_Clicked(self):

      self.RenameLineEdit.setHidden(False)
      self.RenameEnter.setHidden(False)
   
   
      
      
        
      
   def RenameEnter_Clicked(self):
      
      rows =[]
      
      with open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\filenames.csv', 'r') as csvfile:
         csvreader = csv.reader(csvfile)
         for row in csvreader:
            if not(row==[]):
               rows.append(row)

      
      NewName = self.RenameLineEdit.text()
      
      
      rows[selectedMacroPosition][1] = NewName
     

      with open('C:\\Users\\jishjosh08\\Task-Ninja-NEA\\filenames.csv', 'w') as csvfile:
         csvWriter = csv.writer(csvfile)
         csvWriter.writerows(rows)

      self.MacroSlot1.setText(rows[1][1])
   
      self.MacroSlot2.setText(rows[2][1])
      self.MacroSlot3.setText(rows[3][1])
      self.MacroSlot4.setText(rows[4][1])
      self.MacroSlot5.setText(rows[5][1])
      
      
   
   def StopRecordingButton_Clicked(self):
      global recording 
      
      self.RecordingNotRecording.setText('not recording')
      self.StopRecordingButton.setHidden(True)
      end_listeners(keyboard_listener,mouse_listener)
      recording = False
      
   def OverwriteButton_Clicked(self):
      f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'w')
      f.write('\n')
      f.close()

   def AddInputsButton_Clicked(self):

      global recording 

      

      self.RecordingNotRecording.setText('recording')
      self.StopRecordingButton.setHidden(False)
      if not(recording):
         
         listener_thread.start()
      recording = True   
   
   def UserLogScrollBar_Scrolled(self):
      return True #placeholder value        

   
   def OSB_clicked(self): #open settings button 
      return True #placeholder return value for valid parsing 

def addDelay():
   
   global oldtime

   newtime =time.time()
   timepassed = newtime - oldtime
   oldtime = newtime

   timepassed = str(timepassed)
   timepassed = timepassed[0:8]
   timepassed = float(timepassed)

   return timepassed

def on_move(x,y):
   
   if includeMovement == True:
      f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'a')
      f.write(f'({x},{y})\n')
      
      f.write(f'{addDelay()}\n')
      f.close()
   else:
      return True
   
'''def RunMacro():
   
   #print(f'time to run {timesToRunNum}')
   time.sleep(1)
   f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'r')
   
   for i in range(0,timesToRunNum,1):
      f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'r')
      for line in f:
         if setDelays:
            time.sleep(setDelayValue)
         if not HotKeyPressed:
            executeMacroLine(findType(line)[0],findType(line)[1] )
      f.close()       
      #print('end of file ')
   
   f.close()'''
   

def on_click(x,y,button,pressed):
   global skipnext

   f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'a')
   if not skipnext:
      if button == Button.left:
         f.write(f'cl({x},{y})\n')
      elif button == Button.right:
         f.write(f'cr({x},{y})\n')
         
      elif button == Button.middle:
         f.write(f'cm({x},{y})\n')
      skipnext = True
      f.write(f'{addDelay()}\n')
   elif skipnext:
      skipnext = False
   
   f.close()


def on_scroll(x,y,dx,dy):
   f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'a')
   f.write(f'scrolled x:{dx}, y:{dy} \n')
   f.write(f'{addDelay()}\n')
   f.close()
   return True

def on_press(key):
   f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'a')
   f.write(f'pressed {key}\n')
   f.write(f'{addDelay()}\n')
   f.close()
   
def on_release(key):
   f = open(f'C:\\Users\\jishjosh08\\Task-Ninja-NEA\\Macro Logs\\MacroLog{selectedMacroPosition}.txt', 'a')
   f.write(f'released {key}\n')
   f.write(f'{addDelay()}\n')
   f.close()

def hotKeyPressed(key):
   global HotKeyPressed
   
   global recording
   key = str(key)
   
   
   hotkey = 'x'
   hotkey = str(hotkey.replace("'",""))
   
   key = key.replace("'","")
   
   
   if len(hotkey) == 3 and len(key)==3:
      hotkey = hotkey[1]
      key = key[1]
   if key == hotkey:
      ##print(f'hot key pressed ')
      HotKeyPressed = True
  
   if recording and key == hotkey:
      
      end_listeners(keyboard_listener,mouse_listener)
   
      recording = False



keyboard_listener = keyboardListener(on_press=on_press, on_release=on_release)
mouse_listener = mouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
hotKey_listener = keyboardListener(on_press=hotKeyPressed)
  
def start_listeners(keyboard_listener, mouse_listener):
   

   keyboard_listener.start()
   mouse_listener.start()

   #keyboard_listener.join()
   #mouse_listener.join()

def end_listeners(keyboard_listener, mouse_listener):

   keyboard_listener.stop()
   mouse_listener.stop()
   

def overwrite():
   return True

def findType(line):
   isSpecialKey = False
   try:
      if line[1] == '.':
         
         return['delay',float(line)]
      elif line[0:2] == 'cl':
         return ['left click',None]
         
      elif line[0:2] == 'cr':
         return ['right click', None]
      
      elif line[0:2] =='cm':
         return ['middle click',None ]
      
      elif line[0:8] == 'scrolled':
         return['scroll',[line[12],line[19]]]
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
   except IndexError:
      return['unknown',None]
      
def executeMacroLine(type, value):
   
   
   if type == 'left click':
      
      mouse.click(Button.left, 1)
      mouse.release(Button.left)

   elif type == 'right click':

      mouse.click(Button.right, 1 )
      mouse.release(Button.right)

   elif type == 'middle click':

      mouse.click(Button.middle, 1)
      mouse.release(Button.middle)

   elif type == 'scroll':
      mouse.scroll(value[0],value[1])
   
   elif type == 'key':
      time.sleep(0.1)
      keyboard.type(value)
   elif type == 'position':
      mouse.position = (value[0],value[1])

   elif type == 'delay' and not(setDelays):
      time.sleep(value)
      
   elif type == 'unknown':
      print('unknown line type ')

   
   

   
   

   

# Run the listener in a separate thread
listener_thread = threading.Thread(target=start_listeners, daemon=True, args=(keyboard_listener,mouse_listener))
#executor_thread = threading.Thread(target=RunMacro, daemon = True)

hotKey_listener.start()
      

app = QApplication(sys.argv)
window = UI()
app.exec_()

