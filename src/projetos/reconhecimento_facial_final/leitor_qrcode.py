import time
import webbrowser

import cv2
from djitellopy import Tello


NOME_JANELA = "Leitor QR Code - Camera do Drone"


def conectar_drone():
    drone = Tello()

    print("Conectando ao drone Tello...")
    drone.connect()
    print(f"Drone conectado. Bateria: {drone.get_battery()}%")

    print("Ligando camera do drone...")
    drone.streamoff()
    drone.streamon()
    time.sleep(2)

    return drone, drone.get_frame_read()


def desenhar_qr_detectado(frame, pontos):
    if pontos is None:
        return

    pontos = pontos.astype(int)
    for i in range(len(pontos[0])):
        ponto_atual = tuple(pontos[0][i])
        proximo_ponto = tuple(pontos[0][(i + 1) % len(pontos[0])])
        cv2.line(frame, ponto_atual, proximo_ponto, (0, 255, 0), 3)


def rodar_scanner_qr():
    print("\nIniciando leitor de QR Code pela camera do drone...")
    print("Conecte o computador no Wi-Fi do Tello antes de executar.")
    print("Pressione Q ou ESC para sair.")

    drone = None

    try:
        drone, frame_reader = conectar_drone()
        detector_qr = cv2.QRCodeDetector()
        ultimo_qr_lido = ""
        tempo_anterior = time.time()

        cv2.namedWindow(NOME_JANELA, cv2.WINDOW_NORMAL)

        while True:
            frame = frame_reader.frame
            if frame is None:
                time.sleep(0.05)
                continue

            altura, largura, _ = frame.shape
            dados, pontos, _ = detector_qr.detectAndDecode(frame)

            conteudo_qr = "NENHUM QR CODE NA TELA"
            if dados:
                conteudo_qr = dados.strip()
                desenhar_qr_detectado(frame, pontos)

                if conteudo_qr.startswith(("http://", "https://")) and conteudo_qr != ultimo_qr_lido:
                    print(f"\nLink identificado! Abrindo no navegador: {conteudo_qr}")
                    webbrowser.open(conteudo_qr)
                    ultimo_qr_lido = conteudo_qr
                elif conteudo_qr != ultimo_qr_lido:
                    print(f"\nQR Code lido: {conteudo_qr}")
                    ultimo_qr_lido = conteudo_qr

            tempo_atual = time.time()
            fps = 1 / (tempo_atual - tempo_anterior) if tempo_atual > tempo_anterior else 0
            tempo_anterior = tempo_atual

            cv2.rectangle(frame, (0, 0), (largura, 95), (40, 40, 40), cv2.FILLED)
            cv2.putText(frame, f"QR CODE: {conteudo_qr}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"FPS: {int(fps)} | CAMERA: DRONE TELLO | Pressione Q para sair", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 230, 230), 1)

            cv2.imshow(NOME_JANELA, frame)

            tecla = cv2.waitKey(1) & 0xFF
            if tecla == ord("q") or tecla == 27:
                break

    except Exception as erro:
        print(f"Erro ao acessar a camera do drone: {erro}")
        print("Verifique se o PC esta conectado no Wi-Fi do Tello e se o drone esta ligado.")

    finally:
        if drone is not None:
            try:
                drone.streamoff()
            except Exception:
                pass
            drone.end()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    rodar_scanner_qr()