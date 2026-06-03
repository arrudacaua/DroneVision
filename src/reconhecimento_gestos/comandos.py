import cv2
import time
from reconhecimento_gestos.detector import processar_frame_mao, coletar_coordenadas, mapear_dedos_levantados

GESTOS = {
    (1, 1, 1, 1, 1): "Decolar",
    (0, 0, 0, 0, 0): "Parar",
    (1, 0, 0, 0, 0): "Frente",
    (1, 0, 0, 0, 1): "Flip",
    (0, 1, 1, 0, 0): "Trás"
}

def rodar_controle_gestos():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print("Câmera não encontrada")
        return

    h, w, _ = frame.shape
    prev_time = 0
    cv2.namedWindow("Gestos", cv2.WINDOW_NORMAL)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame, results = processar_frame_mao(frame)
            pontos = coletar_coordenadas(results, w, h)
            
            gesto = "Nenhum"
            if pontos:
                dedos = mapear_dedos_levantados(pontos)
                gesto = GESTOS.get(tuple(dedos), "Desconhecido")

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time

            cv2.rectangle(frame, (0, 0), (w, 80), (40, 40, 40), cv2.FILLED)
            cv2.putText(frame, f"Gesto: {gesto}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"FPS: {int(fps)} | Q para sair", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

            cv2.imshow("Gestos", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()