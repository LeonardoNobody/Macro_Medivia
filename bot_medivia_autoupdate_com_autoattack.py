
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

from PIL import ImageOps, ImageEnhance, Image, ImageFilter
from winsound import Beep
from pynput.keyboard import Controller, Key

def preprocess_image(img):
    img = img.convert("L")
    img = img.resize((img.width * 2, img.height * 2))
    img = img.filter(ImageFilter.SHARPEN)
    img = ImageEnhance.Contrast(img).enhance(2)
    return img

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\tibia\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
pynput_keyboard = Controller()

ataque_em_andamento = False  # Compartilhado entre auto_attack e auto_sd
runador_ativo = False
food_ativo = False
sd_disparada = False
ring_ativo = False
verificar_gm_ativo = False
autosd_ativo = False
autoattack_ativo = False  # Novo modo
tempo_ultimo_target = 0
TOLERANCIA_TEMPO = 3

intervalo_runa = 70
intervalo_food = 240
intervalo_ring = 1200
intervalo_sd = 2
intervalo_attack = 1.0  # Intervalo do auto attack

slot_x, slot_y = 1755, 598
cor_slot_vazio = (27, 27, 27)

palavras_chave = [
    "you see", "says", "level", "mage", "high mage", "imperium knight", "royal archer",
    "hp", "mp", "name", "a player", "trade", "guardian druid", "exura ico"
]

pygame.mixer.init()
alerta_som = pygame.mixer.Sound("alerta.wav")

def preprocess_image(img):
    img = img.convert("L")  # tons de cinza
    img = img.resize((img.width * 3, img.height * 3))  # aumenta o tamanho
    img = img.filter(ImageFilter.MedianFilter())  # reduz ruído
    img = ImageEnhance.Contrast(img).enhance(3)  # aumenta contraste
    return img



def cor_igual(c1, c2, tolerancia=5):
    return all(abs(a - b) <= tolerancia for a, b in zip(c1, c2))

def eh_nome_valido(linha):
    linha = linha.lower().strip()
    if len(linha) < 3:
        return False
    if any(p in linha for p in ["lista", "batalha", "a - x", "|", "»", "v"]):
        return False
    if not any(c.isalpha() for c in linha):
        return False
    return True







def tem_target_na_bl():
    global tempo_ultimo_target
    screenshot = pyautogui.screenshot(region=(1529, 336, 190, 288))
    imagem = preprocess_image(screenshot)
    texto = pytesseract.image_to_string(imagem, config='--psm 6')
    linhas = texto.splitlines()
    for linha in linhas:
        if eh_nome_valido(linha.strip()):
            tempo_ultimo_target = time.time()
            return True
    return time.time() - tempo_ultimo_target < TOLERANCIA_TEMPO





def auto_sd():
    while autosd_ativo:
        if ataque_em_andamento:
            keyboard.send('f10')
            print("[AUTO SD] SD disparada")
        else:
            print("[AUTO SD] Aguardando...")
        time.sleep(intervalo_sd)







def auto_attack():
    global ataque_em_andamento
    estava_com_target = False

    while autoattack_ativo:
        try:
            tem_target = tem_target_na_bl()

            if tem_target and not estava_com_target:
                keyboard.send("f3")
                print("[AUTO ATTACK] Alvo detectado — atacando com F3")
                estava_com_target = True
                ataque_em_andamento = True

            elif tem_target and estava_com_target:
                print("[AUTO ATTACK] Ainda com alvo — mantendo ataque")

            elif not tem_target and estava_com_target:
                print("[AUTO ATTACK] Alvo sumiu — encerrando ataque")
                estava_com_target = False
                ataque_em_andamento = False

        except Exception as e:
            print(f"[ERRO] Auto Attack falhou: {e}")
        time.sleep(intervalo_attack)






def iniciar_autosd():
    global autosd_ativo
    autosd_ativo = True
    threading.Thread(target=auto_sd, daemon=True).start()
    status_autosd.config(text="Auto SD: Ativo", fg="green")

def parar_autosd():
    global autosd_ativo
    autosd_ativo = False
    status_autosd.config(text="Auto SD: Parado", fg="red")

def iniciar_autoattack():
    global autoattack_ativo
    autoattack_ativo = True
    threading.Thread(target=auto_attack, daemon=True).start()
    status_autoattack.config(text="Auto Attack: Ativo", fg="green")

def parar_autoattack():
    global autoattack_ativo
    autoattack_ativo = False
    status_autoattack.config(text="Auto Attack: Parado", fg="red")

def atualizar_tempo_sd(val): global intervalo_sd; intervalo_sd = int(val)
def atualizar_tempo_attack(val): global intervalo_attack; intervalo_attack = float(val)

def monitorar_battle_list():
    global verificar_gm_ativo
    while verificar_gm_ativo:
        screenshot = pyautogui.screenshot(region=(1529, 336, 190, 288))
        imagem = screenshot.convert('L')
        imagem = preprocess_image(imagem)
        imagem.save("debug_battlelist.png")
        texto = pytesseract.image_to_string(imagem, config='--psm 6')
        print("[OCR] Resultado completo:\n", texto)
        linhas = texto.splitlines()
        for linha in linhas:
            linha = linha.strip()
            print(f"[DEBUG] OCR linha: '{linha}'")
            if eh_nome_valido(linha):
                print("[⚠️ ALERTA] Presença detectada na Battle List!")
                if alerta_som:
                    alerta_som.play()
                else:
                    Beep(1000, 500)
                time.sleep(1.5)
                janela.destroy()
                sys.exit(0)
        time.sleep(2)

def iniciar_monitoramento_ocr():
    threading.Thread(target=monitorar_battle_list, daemon=True).start()

# Interface
janela = tk.Tk()
janela.title("Bot Medivia HUD")
janela.geometry("220x720+1650+200")
janela.configure(bg="#f2f2f2")
janela.attributes("-topmost", True)
janela.overrideredirect(True)

def iniciar_movimento(event): janela.x = event.x; janela.y = event.y
def movimentar(event): x = janela.winfo_pointerx() - janela.x; y = janela.winfo_pointery() - janela.y; janela.geometry(f"+{x}+{y}")
barra_superior = tk.Frame(janela, bg="#cccccc", height=20); barra_superior.pack(fill="x")
barra_superior.bind("<Button-1>", iniciar_movimento); barra_superior.bind("<B1-Motion>", movimentar)
btn_fechar = tk.Button(barra_superior, text="X", command=janela.destroy, bg="red", fg="white", bd=0); btn_fechar.pack(side="right", padx=2, pady=1)

fonte_titulo = ("Segoe UI", 10, "bold")
fonte_padrao = ("Segoe UI", 8)

tk.Label(janela, text="Medivia HUD Bot", font=fonte_titulo, bg="#f2f2f2").pack(pady=8)
tk.Label(janela, text="Auto SD (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_sd = tk.Scale(janela, from_=1, to=10, orient=tk.HORIZONTAL, command=atualizar_tempo_sd, bg="#e6e6e6"); slider_sd.set(intervalo_sd); slider_sd.pack()
tk.Button(janela, text="Iniciar Auto SD", command=iniciar_autosd, bg="#4CAF50", fg="white").pack()
tk.Button(janela, text="Parar Auto SD", command=parar_autosd, bg="#f44336", fg="white").pack()
status_autosd = tk.Label(janela, text="Auto SD: Parado", fg="red", bg="#f2f2f2"); status_autosd.pack()

tk.Label(janela, text="Auto Attack (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_attack = tk.Scale(janela, from_=0.1, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, command=atualizar_tempo_attack, bg="#e6e6e6")
slider_attack.set(intervalo_attack); slider_attack.pack()
tk.Button(janela, text="Iniciar Auto Attack", command=iniciar_autoattack, bg="#4CAF50", fg="white").pack()
tk.Button(janela, text="Parar Auto Attack", command=parar_autoattack, bg="#f44336", fg="white").pack()
status_autoattack = tk.Label(janela, text="Auto Attack: Parado", fg="red", bg="#f2f2f2"); status_autoattack.pack()

tk.Button(janela, text="Detectar Players (OCR)", command=iniciar_monitoramento_ocr, bg="#2196F3", fg="white").pack()
status_gm = tk.Label(janela, text="❌ GM: Desligado", fg="red", bg="#f2f2f2"); status_gm.pack()

janela.mainloop()
