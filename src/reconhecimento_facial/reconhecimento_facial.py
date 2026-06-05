import cv2
import face_recognition
from djitellopy import Tello
import os
import time
import numpy as np

rostos_conhecidos = []
nomes_conhecidos = []

pasta = "rostos"

for pessoa in os.listdir(pasta):

    caminho_pessoa = os.path.join(pasta, pessoa)

    if not os.path.isdir(caminho_pessoa):
        continue

    for arquivo in os.listdir(caminho_pessoa):

        caminho_imagem = os.path.join(
            caminho_pessoa,
            arquivo
        )

        imagem = face_recognition.load_image_file(
            caminho_imagem
        )

        encodings = face_recognition.face_encodings(
            imagem
        )

        if len(encodings) > 0:

            rostos_conhecidos.append(
                encodings[0]
            )

            nomes_conhecidos.append(
                pessoa
            )

print(
    "Rostos carregados:",
    len(rostos_conhecidos)
)

drone = Tello()

drone.connect()

print(
    "Bateria:",
    drone.get_battery(),
    "%"
)

drone.streamoff()
drone.streamon()

time.sleep(2)

frame_reader = drone.get_frame_read()

contador = 0

locais = []
nomes = []

while True:

    frame = frame_reader.frame
    

    if frame is None:
        continue

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2BGR
    )

    frame = cv2.resize(
        frame,
        (320, 240)
    )

    contador += 1

    if contador % 30 == 0:

        small = cv2.resize(
            frame,
            (0, 0),
            fx=0.5,
            fy=0.5
        )

        rgb_small = cv2.cvtColor(
            small,
            cv2.COLOR_BGR2RGB
        )

        novos_locais = face_recognition.face_locations(
            rgb_small
        )

        novos_encodings = face_recognition.face_encodings(
            rgb_small,
            novos_locais
        )

        locais = []
        nomes = []

        for encoding, (
            top,
            right,
            bottom,
            left
        ) in zip(
            novos_encodings,
            novos_locais
        ):

            nome = "Desconhecido"

            matches = face_recognition.compare_faces(
                rostos_conhecidos,
                encoding,
                tolerance=0.5
            )

            distancias = face_recognition.face_distance(
                rostos_conhecidos,
                encoding
            )

            if len(distancias) > 0:

                melhor = np.argmin(
                    distancias
                )

                if matches[melhor]:

                    nome = nomes_conhecidos[
                        melhor
                    ]

            locais.append(
                (
                    top * 2,
                    right * 2,
                    bottom * 2,
                    left * 2
                )
            )

            nomes.append(nome)

    for (
        top,
        right,
        bottom,
        left
    ), nome in zip(
        locais,
        nomes
    ):

        cv2.rectangle(
            frame,
            (left, top),
            (right, bottom),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            nome,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow(
        "Face Recognition - Tello",
        frame
    )

    if cv2.waitKey(1) & 0xFF == 27:
        break

drone.streamoff()
cv2.destroyAllWindows()