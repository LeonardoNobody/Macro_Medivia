import pyautogui
import time

def capturar_coordenadas():
    print("🚀 POSICIONAMENTO INICIADO")
    print("➡️  Passe o mouse sobre o **TOPO da Battle List** e aguarde...")
    time.sleep(3)
    topo = pyautogui.position()
    print(f"📌 Topo: {topo}")

    print("\n➡️  Agora passe o mouse sobre o **CANTO INFERIOR DIREITO** da Battle List e aguarde...")
    time.sleep(3)
    base = pyautogui.position()
    print(f"📌 Base: {base}")

    largura = base.x - topo.x
    altura = base.y - topo.y
    print("\n✅ Região calculada para o pyautogui:")
    print(f"region = ({topo.x}, {topo.y}, {largura}, {altura})")

    # Captura imagem da região para verificação
    screenshot = pyautogui.screenshot(region=(topo.x, topo.y, largura, altura))
    screenshot.save("regiao_battlelist_debug.png")
    print("\n🖼️ Imagem salva como regiao_battlelist_debug.png")

if __name__ == "__main__":
    capturar_coordenadas()
