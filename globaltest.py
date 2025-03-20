from pynput import keyboard
def on_press(key):
        
    print(key)

while True:
    
    keyboardlistener = keyboard.Listener(on_press = on_press)
    keyboardlistener.start()