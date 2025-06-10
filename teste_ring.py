import tkinter as tk
import threading
import time
import pyautogui
import keyboard
from pynput.keyboard import Controller, Key

# Controlador do teclado via pynput
pynput_keyboard = Controller()

# Flags de execução
runador_ativo = False
food_ativo = False
ring_ativo = False

# Intervalos (valores padrão)
intervalo_runa = 70
intervalo_food = 240
intervalo_ring = 1200  # 20 minutos

# Magia a ser usada no Runador
magia_para_runar = "incuro vita"

# Coordenadas e cor do slot do ring vazio
slot_x, slot_y = 1755, 598
cor_slot_vazio = (27, 27, 27)

def cor_igual(c1, c2, tolerancia=5):
    return all(abs(a - b) <= tolerancia for a, b in zip(c1, c2))

def runador():
    global runador_ativo
    while runador_ativo:
        keyboard.write(magia_para_runar)           # Digita a magia
        time.sleep(0.2)                             # Dá um tempo pequeno para garantir que digitou tudo
        keyboard.press_and_release('enter')        # Pressiona Enter
        print(f"[RUNADOR] Magia '{magia_para_runar}' lançada - aguardando {intervalo_runa}s")
        time.sleep(intervalo_runa)


def auto_food():
    global food_ativo
    while food_ativo:
        pynput_keyboard.press(Key.f11)
        pynput_keyboard.release(Key.f11)
        print(f"[AUTO FOOD] F11 pressionado - aguardando {intervalo_food}s")
        time.sleep(intervalo_food)

def auto_ring():
    global ring_ativo
    while ring_ativo:
        cor_atual = pyautogui.pixel(slot_x, slot_y)
        if cor_igual(cor_atual, cor_slot_vazio):
            keyboard.press_and_release('f9')
            print(f"[AUTO RING] Slot vazio detectado. F9 pressionado - aguardando {intervalo_ring}s")
        else:
            print("[AUTO RING] Slot ainda ocupado. Nenhuma ação tomada.")
        time.sleep(intervalo_ring)

# Início e parada
def iniciar_runador():
    global runador_ativo, magia_para_runar
    magia_para_runar = campo_magia.get() or "exura"
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

def atualizar_tempo_runa(val): global intervalo_runa; intervalo_runa = int(val)
def atualizar_tempo_food(val): global intervalo_food; intervalo_food = int(val)
def atualizar_tempo_ring(val): global intervalo_ring; intervalo_ring = int(val)

# Interface
janela = tk.Tk()
janela.title("Bot Medivia - Deluxe 🧙‍♂️")
janela.geometry("360x580")
janela.configure(bg="#f2f2f2")

fonte_titulo = ("Segoe UI", 14, "bold")
fonte_padrao = ("Segoe UI", 10)

# Título
tk.Label(janela, text="Bot Medivia AFK", font=fonte_titulo, bg="#f2f2f2").pack(pady=10)

# Campo da Magia
tk.Label(janela, text="Magia para runar (ex: exura, adori vita vis):", font=fonte_padrao, bg="#f2f2f2").pack()
campo_magia = tk.Entry(janela, font=fonte_padrao, justify="center")
campo_magia.insert(0, magia_para_runar)
campo_magia.pack(pady=(0, 10))

# Runador
tk.Label(janela, text="Tempo entre Runas (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_runa = tk.Scale(janela, from_=10, to=1800, orient=tk.HORIZONTAL, command=atualizar_tempo_runa, bg="#e6e6e6")
slider_runa.set(intervalo_runa)
slider_runa.pack()
tk.Button(janela, text="Iniciar Runador", command=iniciar_runador, bg="#4CAF50", fg="white").pack(pady=3)
tk.Button(janela, text="Parar Runador", command=parar_runador, bg="#f44336", fg="white").pack()
status_runador = tk.Label(janela, text="Runador: Parado", fg="red", bg="#f2f2f2")
status_runador.pack(pady=(0, 10))

# Auto Food
tk.Label(janela, text="Tempo entre Comidas (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_food = tk.Scale(janela, from_=10, to=1800, orient=tk.HORIZONTAL, command=atualizar_tempo_food, bg="#e6e6e6")
slider_food.set(intervalo_food)
slider_food.pack()
tk.Button(janela, text="Iniciar Auto Food", command=iniciar_food, bg="#4CAF50", fg="white").pack(pady=3)
tk.Button(janela, text="Parar Auto Food", command=parar_food, bg="#f44336", fg="white").pack()
status_food = tk.Label(janela, text="Auto Food: Parado", fg="red", bg="#f2f2f2")
status_food.pack(pady=(0, 10))

# Auto Ring
tk.Label(janela, text="Tempo entre checagens do Ring (s)", font=fonte_padrao, bg="#f2f2f2").pack()
slider_ring = tk.Scale(janela, from_=10, to=1800, orient=tk.HORIZONTAL, command=atualizar_tempo_ring, bg="#e6e6e6")
slider_ring.set(intervalo_ring)
slider_ring.pack()
tk.Button(janela, text="Iniciar Auto Ring", command=iniciar_ring, bg="#4CAF50", fg="white").pack(pady=3)
tk.Button(janela, text="Parar Auto Ring", command=parar_ring, bg="#f44336", fg="white").pack()
status_ring = tk.Label(janela, text="Auto Ring: Parado", fg="red", bg="#f2f2f2")
status_ring.pack(pady=(0, 10))

janela.mainloop()
