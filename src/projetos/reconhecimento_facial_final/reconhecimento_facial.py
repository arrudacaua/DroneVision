import os
import sys
import time
import cv2
import numpy as np
import face_recognition
from djitellopy import Tello

PASTA_ROSTOS = "rostos"
TOLERANCIA = 0.5
ESCALA_PROCESSAMENTO = 0.25


def carregar_rostos():
    rostos_conhecidos = []
    nomes_conhecidos = []

    if not os.path.exists(PASTA_ROSTOS):
        print("ERRO: pasta 'rostos' nao encontrada.")
        return rostos_conhecidos, nomes_conhecidos

    for pessoa in os.listdir(PASTA_ROSTOS):
        caminho_pessoa = os.path.join(PASTA_ROSTOS, pessoa)

        if not os.path.isdir(caminho_pessoa):
            continue

        for arquivo in os.listdir(caminho_pessoa):
            if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            caminho_imagem = os.path.join(caminho_pessoa, arquivo)

            try:
                imagem = face_recognition.load_image_file(caminho_imagem)
                encodings = face_recognition.face_encodings(imagem)

                if len(encodings) > 0:
                    rostos_conhecidos.append(encodings[0])
                    nomes_conhecidos.append(pessoa.replace("_", " "))
                    print(f"Foto carregada: {pessoa}/{arquivo}")
                else:
                    print(f"Nenhum rosto encontrado em: {pessoa}/{arquivo}")

            except Exception as erro:
                print(f"Erro ao carregar {caminho_imagem}: {erro}")

    return rostos_conhecidos, nomes_conhecidos


def reconhecer_rosto(encoding, rostos_conhecidos, nomes_conhecidos):
    nome = "Desconhecido"

    if len(rostos_conhecidos) == 0:
        return nome

    comparacoes = face_recognition.compare_faces(
        rostos_conhecidos,
        encoding,
        tolerance=TOLERANCIA
    )

    distancias = face_recognition.face_distance(
        rostos_conhecidos,
        encoding
    )

    melhor = np.argmin(distancias)

    if comparacoes[melhor]:
        nome = nomes_conhecidos[melhor]

    return nome


def conectar_drone():
    print("Conectando ao Drone Tello...")

    drone = Tello()
    drone.connect()

    bateria = drone.get_battery()
    print(f"Drone conectado. Bateria: {bateria}%")

    drone.streamoff()
    drone.streamon()

    time.sleep(2)

    return drone


def rodar_reconhecimento_facial():
    print("Carregando rostos cadastrados...")
    rostos_conhecidos, nomes_conhecidos = carregar_rostos()
    print("Rostos carregados:", len(rostos_conhecidos))

    drone = conectar_drone()
    frame_reader = drone.get_frame_read()

    print("Camera do drone aberta. Aperte ESC para sair.")

    try:
        while True:
            frame = frame_reader.frame

            if frame is None:
                continue

            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            frame_pequeno = cv2.resize(
                frame,
                (0, 0),
                fx=ESCALA_PROCESSAMENTO,
                fy=ESCALA_PROCESSAMENTO
            )

            frame_rgb = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)

            locais = face_recognition.face_locations(frame_rgb)
            encodings = face_recognition.face_encodings(frame_rgb, locais)

            for encoding, (top, right, bottom, left) in zip(encodings, locais):
                nome = reconhecer_rosto(
                    encoding,
                    rostos_conhecidos,
                    nomes_conhecidos
                )

                top = int(top / ESCALA_PROCESSAMENTO)
                right = int(right / ESCALA_PROCESSAMENTO)
                bottom = int(bottom / ESCALA_PROCESSAMENTO)
                left = int(left / ESCALA_PROCESSAMENTO)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                cv2.putText(
                    frame,
                    nome,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Reconhecimento Facial - Drone Tello", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    except KeyboardInterrupt:
        print("Programa interrompido pelo usuario.")

    finally:
        print("Encerrando camera do drone...")
        drone.streamoff()
        drone.end()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        rodar_reconhecimento_facial()
    except Exception as erro:
        print("\nERRO:")
        print(erro)
        print("\nVerifique se:")
        print("1. O computador esta conectado ao Wi-Fi do drone Tello.")
        print("2. A biblioteca djitellopy esta instalada.")
        print("3. Nenhum outro programa esta usando o drone.")
        sys.exit(1)