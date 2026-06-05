import sys
import os

caminho_atual = os.path.dirname(os.path.abspath(__file__))
if caminho_atual.endswith("src"):
    sys.path.append(caminho_atual)
    sys.path.append(os.path.dirname(caminho_atual))
else:
    sys.path.append(os.path.join(caminho_atual, "src"))
    sys.path.append(caminho_atual)

from djitellopy import Tello
from reconhecimento_gestos.comandos import rodar_controle_gestos
from escaneamento_qrcode.leitor_qrcode import rodar_scanner_qr

def menu():
    print("\n" + "="*40)
    print("DRONE VISION")
    print("="*40)
    print("1 - Controle por Gestos")
    print("2 - Reconhecimento Facial")
    print("3 - QR Code (Teste Local / Drone)")
    print("4 - Rotas Automatizadas")
    print("0 - Sair")
    print("="*40)

def main():
    print("Tentando conectar ao Drone Tello...")
    try:
        drone = Tello()
        drone.connect()
        print(f"Drone conectado com sucesso! Bateria atual: {drone.get_battery()}%")
    except Exception as e:
        print("\n⚠️ Não foi possível estabelecer conexão com o drone físico.")
        print("O sistema entrará automaticamente no MODO DE TESTES DA WEBCAM DO PC.")
        drone = None 

    while True:
        menu()
        opcao = input("Opção: ").strip()

        if opcao == "1":
            try:
                rodar_controle_gestos(drone)
            except Exception as e:
                print(f"Erro no módulo de gestos: {e}")
                
        elif opcao == "2":
            print("Em desenvolvimento...")
            
        elif opcao == "3":
            try:
                rodar_scanner_qr(drone)
            except Exception as e:
                print(f"Erro no Scanner QR: {e}")
                
        elif opcao == "4":
            print("Em desenvolvimento...")
            
        elif opcao == "0":
            print("Encerrando o Drone Vision...")
            if drone:
                drone.end() 
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()