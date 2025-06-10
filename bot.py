import tkinter as tk
import re
import threading
import time
import pyautogui
import pytesseract
import keyboard
import pygame
import string
import sys
import os

from PIL import ImageOps, ImageEnhance
from winsound import Beep
from pynput.keyboard import Controller, Key

def preprocess_image(img):
    from PIL import ImageEnhance, ImageFilter

    img = img.convert("L")
    img = img.resize((img.width * 2, img.height * 2))  # aumenta detalhes
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(2)
    return img





# Caminho do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\tibia\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"

# Controlador do teclado
pynput_keyboard = Controller()

# Flags
runador_ativo = False
food_ativo = False
ring_ativo = False
verificar_gm_ativo = False

# Intervalos
intervalo_runa = 70
intervalo_food = 240
intervalo_ring = 1200

# Slot ring
slot_x, slot_y = 1755, 598
cor_slot_vazio = (27, 27, 27)

# Palavras-chave para detectar player/GM
palavras_chave = [
    "you see", "says", "level", "mage", "high mage", "imperium knight", "royal archer",
    "hp", "mp", "name", "a player", "trade", "guardian druid", "exura ico"
]

# Alerta sonoro


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inicializar o mixer ANTES de carregar o som
pygame.mixer.init()
alerta_som = pygame.mixer.Sound(resource_path("alerta.wav"))


def cor_igual(c1, c2, tolerancia=5):
    return all(abs(a - b) <= tolerancia for a, b in zip(c1, c2))

linhas_detectadas = set()

def eh_nome_valido(linha):
    # Remove ruídos comuns do começo
    linha = linha.lstrip(string.punctuation + "¢¥%*=!<>\"'|·")

    palavras = linha.strip().split()

    if len(palavras) == 0:
        return False

    # Se tiver "lista de batalha" ou palavras comuns do layout, ignora
    if "lista" in linha.lower() or "batalha" in linha.lower():
        return False

    # Se menos de 60% da linha for letra, descarta (evita ruído)
    letras = sum(c.isalpha() for c in linha)
    if letras / max(len(linha), 1) < 0.6:
        return False

    # Pelo menos 1 palavra deve começar com maiúscula e conter só letras
    palavras_validas = [p for p in palavras if p.istitle() and p.isalpha()]
    return len(palavras_validas) >= 1

def monitorar_battle_list():
    while verificar_gm_ativo:
        screenshot = pyautogui.screenshot(region=(1529, 336, 190, 288))
        imagem = screenshot.convert('L')
        imagem = preprocess_image(imagem)
        imagem.save("debug_battlelist.png")
        texto = pytesseract.image_to_string(imagem, config='--psm 6')
        print("[OCR] Resultado completo:\n", texto)

        linhas = texto.splitlines()
        presenca_detectada = False

        for linha in linhas:
            linha = linha.strip()
            print(f"[DEBUG] OCR linha: '{linha}'")
            if eh_nome_valido(linha):
                presenca_detectada = True
                break

        if presenca_detectada:
            print("[⚠️ ALERTA] Presença detectada na Battle List!")
            while verificar_gm_ativo and presenca_detectada:
                Beep(1000, 500)
                time.sleep(0.5)

                # Nova checagem para continuar beepando
                screenshot = pyautogui.screenshot(region=(1529, 336, 190, 288))
  # só a primeira linha
                screenshot.save("debug_battlelist.png")
                imagem = screenshot.convert('L')
                imagem = preprocess_image(imagem)
                texto = pytesseract.image_to_string(imagem, config='--psm 6')
                linhas = texto.splitlines()

                presenca_detectada = False
                for linha in linhas:
                    linha = linha.strip()
                    if eh_nome_valido(linha):
                        presenca_detectada = True
                        break
        else:
            time.sleep(2)



def iniciar_monitoramento_ocr():
    threading.Thread(target=monitorar_battle_list, daemon=True).start()


def runador():
    while runador_ativo:
        pynput_keyboard.press(Key.f12)
        pynput_keyboard.release(Key.f12)
        print(f"[RUNADOR] F12 pressionado - aguardando {intervalo_runa}s")
        time.sleep(intervalo_runa)

def auto_food():
    while food_ativo:
        pynput_keyboard.press(Key.f11)
        pynput_keyboard.release(Key.f11)
        print(f"[AUTO FOOD] F11 pressionado - aguardando {intervalo_food}s")
        time.sleep(intervalo_food)

def auto_ring():
    while ring_ativo:
        cor_atual = pyautogui.pixel(slot_x, slot_y)
        if cor_igual(cor_atual, cor_slot_vazio):
            keyboard.press_and_release('f9')
            print(f"[AUTO RING] Slot vazio detectado. F9 pressionado - aguardando {intervalo_ring}s")
        else:
            print("[AUTO RING] Slot ainda ocupado.")
        time.sleep(intervalo_ring)

def iniciar_runador():
    global runador_ativo
    runador_ativo = True
    threading.Thread(target=runador, daemon=True).start()
    status_runador.config(text="Runador: Ativo", fg="green")

def parar_runador():
    global runador_ativo
    runador_ativo = False
    status_runador.config(text="Runador: Parado", fg="red")

def iniciar_food():
    global food_ativo
    food_ativo = True
    threading.Thread(target=auto_food, daemon=True).start()
    status_food.config(text="Auto Food: Ativo", fg="green")

def parar_food():
    global food_ativo
    food_ativo = False
    status_food.config(text="Auto Food: Parado", fg="red")

def iniciar_ring():
    global ring_ativo
    ring_ativo = True
    threading.Thread(target=auto_ring, daemon=True).start()
    status_ring.config(text="Auto Ring: Ativo", fg="green")

def parar_ring():
    global ring_ativo
    ring_ativo = False
    status_ring.config(text="Auto Ring: Parado", fg="red")

def alternar_verificacao_gm():
    global verificar_gm_ativo
    verificar_gm_ativo = not verificar_gm_ativo
    if verificar_gm_ativo:
        iniciar_monitoramento_ocr()
    texto = "✔️ GM: Ativo" if verificar_gm_ativo else "❌ GM: Desligado"
    status_gm.config(text=texto, fg="green" if verificar_gm_ativo else "red")

def atualizar_tempo_runa(val): global intervalo_runa; intervalo_runa = int(val)
def atualizar_tempo_food(val): global intervalo_food; intervalo_food = int(val)
def atualizar_tempo_ring(val): global intervalo_ring; intervalo_ring = int(val)

# GUI estilo HUD
janela = tk.Tk()
janela.title("Bot Medivia HUD")
janela.geometry("220x530+1650+200")
janela.configure(bg="#f2f2f2")
janela.attributes("-topmost", True)
janela.overrideredirect(True)  # Remove bordas

# Função de movimentação (arrasto da HUD)
def iniciar_movimento(event):
    janela.x = event.x
    janela.y = event.y

def movimentar(event):
    x = janela.winfo_pointerx() - janela.x
    y = janela.winfo_pointery() - janela.y
    janela.geometry(f"+{x}+{y}")

# Barra superior para mover e fechar
barra_superior = tk.Frame(janela, bg="#cccccc", height=20)
barra_superior.pack(fill="x")
barra_superior.bind("<Button-1>", iniciar_movimento)
barra_superior.bind("<B1-Motion>", movimentar)

btn_fechar = tk.Button(barra_superior, text="X", command=janela.destroy, bg="red", fg="white", bd=0)
btn_fechar.pack(side="right", padx=2, pady=1)

fonte_titulo = ("Segoe UI", 10, "bold")
fonte_padrao = ("Segoe UI", 8)

tk.Label(janela, text="Medivia HUD Bot", font=fonte_titulo, bg="#f2f2f2").pack(pady=8)

tk.Label(janela, text="Runas (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_runa = tk.Scale(janela, from_=10, to=1800, orient=tk.HORIZONTAL, command=atualizar_tempo_runa, bg="#e6e6e6")
slider_runa.set(intervalo_runa); slider_runa.pack()
tk.Button(janela, text="Iniciar Runador", command=iniciar_runador, bg="#4CAF50", fg="white").pack()
tk.Button(janela, text="Parar Runador", command=parar_runador, bg="#f44336", fg="white").pack()
status_runador = tk.Label(janela, text="Runador: Parado", fg="red", bg="#f2f2f2"); status_runador.pack()

tk.Label(janela, text="Food (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_food = tk.Scale(janela, from_=10, to=1800, orient=tk.HORIZONTAL, command=atualizar_tempo_food, bg="#e6e6e6")
slider_food.set(intervalo_food); slider_food.pack()
tk.Button(janela, text="Iniciar Auto Food", command=iniciar_food, bg="#4CAF50", fg="white").pack()
tk.Button(janela, text="Parar Auto Food", command=parar_food, bg="#f44336", fg="white").pack()
status_food = tk.Label(janela, text="Auto Food: Parado", fg="red", bg="#f2f2f2"); status_food.pack()

tk.Label(janela, text="Ring (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_ring = tk.Scale(janela, from_=10, to=1800, orient=tk.HORIZONTAL, command=atualizar_tempo_ring, bg="#e6e6e6")
slider_ring.set(intervalo_ring); slider_ring.pack()
tk.Button(janela, text="Iniciar Auto Ring", command=iniciar_ring, bg="#4CAF50", fg="white").pack()
tk.Button(janela, text="Parar Auto Ring", command=parar_ring, bg="#f44336", fg="white").pack()
status_ring = tk.Label(janela, text="Auto Ring: Parado", fg="red", bg="#f2f2f2"); status_ring.pack()

tk.Button(janela, text="Detectar Players (OCR)", command=alternar_verificacao_gm, bg="#2196F3", fg="white").pack()
status_gm = tk.Label(janela, text="❌ GM: Desligado", fg="red", bg="#f2f2f2"); status_gm.pack()

janela.mainloop()
