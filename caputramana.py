import pytesseract
import pyautogui
import threading
import time
from pynput.keyboard import Controller, Key
from PIL import Image

# Configuração do caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\tibia\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Teclado para enviar comandos
keyboard = Controller()

# Flag de controle
runa_ativa = True

# Região da mana (ajuste se necessário)
# (x, y, largura, altura)
regiao_mana = (1800, 413, 90, 25)  # você pode ajustar largura e altura se necessário

def detectar_mana():
    screenshot = pyautogui.screenshot(region=regiao_mana)
    imagem = screenshot.convert('L')  # preto e branco
    imagem.save("debug_mana.png")  # <- novo
    texto = pytesseract.image_to_string(imagem, config='--psm 7').strip()
    print(f"[OCR] Texto reconhecido: {texto}")
    ...

    
    try:
        mana_atual = int(texto.split("/")[0].strip())  # pega só a mana atual
        return mana_atual
    except:
        return 0  # caso OCR falhe

def runador_automatizado():
    global runa_ativa
    while runa_ativa:
        mana = detectar_mana()
        if mana >= 1800:
            print(f"[RUNADOR] Mana = {mana}. Iniciando spam por 15s...")
            fim = time.time() + 15
            while time.time() < fim:
                keyboard.press(Key.f12)
                keyboard.release(Key.f12)
                time.sleep(0.3)
            print("[RUNADOR] Spam finalizado. Aguardando regeneração.")
        else:
            print(f"[RUNADOR] Mana = {mana}. Aguardando...")
        time.sleep(5)

# Início da thread
threading.Thread(target=runador_automatizado, daemon=True).start()
