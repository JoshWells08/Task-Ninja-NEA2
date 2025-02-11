from pynput import mouse

def on_move(x, y):
    print(f"Mouse moved to ({x}, {y})")

def on_click(x, y, button, pressed):
    action = "Pressed" if pressed else "Released"
    print(f"Mouse {action} at ({x}, {y}) with {button}")

def on_scroll(x, y, dx, dy):
    print(f"Scrolled at ({x}, {y}) by ({dx}, {dy})")

# Start the listener
with mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    print("Mouse listener started. Move/click/scroll to test...")
    listener.join()
