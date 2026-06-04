import sys
import os
from djitellopy import Tello # IMPORTAÇÃO DO DRONE
from reconhecimento_gestos.comandos import rodar_controle_gestos

def menu():
    print("\n" + "="*40)
    print("DRONE VISION")
    print("="*40)
    print("1 - Controle por Gestos")
    print("2 - Reconhecimento Facial")
    print("3 - QR Code")
    print("4 - Rotas Automatizadas")
    print("0 - Sair")
    print("="*40)

def main():
    # 🛸 Inicializa e conecta o drone assim que o programa abre
    print("Conectando ao Drone Tello...")
    try:
        drone = Tello()
        drone.connect()
        print(f"Drone conectado! Bateria atual: {drone.get_battery()}%")
    except Exception as e:
        print(f"⚠️ Não foi possível conectar ao drone físico: {e}")
        print("O programa continuará rodando em modo de simulação (apenas exibindo comandos).")
        drone = None # Se falhar, define como None para não crashar o menu

    while True:
        menu()
        opcao = input("Opção: ").strip()

        if opcao == "1":
            try:
                # Passa o objeto do drone para o módulo de gestos
                rodar_controle_gestos(drone)
            except Exception as e:
                print(f"Erro: {e}")
        elif opcao == "2":
            print("Em desenvolvimento...")
        elif opcao == "3":
            print("Em desenvolvimento...")
        elif opcao == "4":
            print("Em desenvolvimento...")
        elif opcao == "0":
            print("Encerrando...")
            # Desconecta o drone de forma segura antes de fechar o programa
            if drone:
                drone.end() 
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()