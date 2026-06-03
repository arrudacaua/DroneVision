import sys
import os
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
    while True:
        menu()
        opcao = input("Opção: ").strip()

        if opcao == "1":
            try:
                rodar_controle_gestos()
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
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()