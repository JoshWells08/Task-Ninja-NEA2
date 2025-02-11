import sys
import threading
from pynput import mouse, keyboard
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QScrollArea, QScrollBar

recording = False
macroSlot1Name = 'MacroLog1'
filehandler = 'placeholder'


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi('MainMenu.ui', self)

        '''Initialize widgets in program'''
        self.CreateNewMacroButton = self.findChild(QPushButton, 'CreateNewMacro')
        self.RunExistingMacroButton = self.findChild(QPushButton, 'RunExistingMacro')
        self.OpenSettingsButton = self.findChild(QPushButton, 'OpenSettings')
        self.BackgroundImage = self.findChild(QLabel, 'BackgroundImage')
        self.show()  # Display widgets

        '''Set event handlers'''
        self.CreateNewMacroButton.clicked.connect(self.CNMB_clicked)
        self.RunExistingMacroButton.clicked.connect(self.REMB_clicked)
        self.OpenSettingsButton.clicked.connect(self.OSB_clicked)

    '''Define events'''

    def CNMB_clicked(self):
        uic.loadUi('CreateNewMacro.ui', self)

        '''Initialize widgets within program'''
        self.UserLogArea = self.findChild(QScrollArea, 'UserLogArea')
        self.UserLog = self.findChild(QLabel, 'UserLog')
        self.UserLogScrollBar = self.findChild(QScrollBar, 'UserLogScrollBar')
        self.RecordingNotRecording = self.findChild(QLabel, 'RecordingNotRecording')
        self.StopRecordingButton = self.findChild(QPushButton, 'StopRecordingButton')
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

        self.show()  # Display widgets

        '''Set event handlers'''
        self.MacroSlot1.clicked.connect(self.MacroSlot1_Clicked)
        self.UserLogScrollBar.sliderMoved.connect(self.UserLogScrollBar_Scrolled)

    def MacroSlot1_Clicked(self):
        global f
        f = open(r'C:\Users\jishjosh08\Task-Ninja-NEA\Macro Logs\MacroLog1.txt', 'a')

    def UserLogScrollBar_Scrolled(self):
        return True  # Placeholder value        

    def REMB_clicked(self):  # Run existing macro button
        return True  # Placeholder return value

    def OSB_clicked(self):  # Open settings button
        return True  # Placeholder return value


''' Define mouse and keyboard event handlers outside of UI class '''


def on_move(x, y):
    print(f'moved to position({x},{y})')
    f = open(r'C:\Users\jishjosh08\Task-Ninja-NEA\Macro Logs\MacroLog1.txt', 'a')
    f.write(f'moved to position({x},{y})')


def on_click(x, y, button, pressed):
    print('clicked')


def on_scroll(x, y, dx, dy):
    print('scrolled')


def on_press(key):
    print(f'{key} pressed')


def on_release(key):
    print(f'{key} released')


''' Start listeners in a separate thread '''


def start_listeners():
    keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

    keyboard_listener.start()
    mouse_listener.start()

    keyboard_listener.join()
    mouse_listener.join()


# Run the listener in a separate thread
listener_thread = threading.Thread(target=start_listeners, daemon=True)
listener_thread.start()

# Start the PyQt application
app = QApplication(sys.argv)
window = UI()
app.exec_()
