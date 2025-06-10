from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

print("Apertando F3 em 3 segundos...")
time.sleep(3)
keyboard.press(Key.f3)
keyboard.release(Key.f3)
print("F3 enviado")
