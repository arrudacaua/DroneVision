import cv2
import time
from reconhecimento_gestos.detector import processar_frame_mao, coletar_coordenadas, mapear_dedos_levantados

DICIONARIO_COMANDOS = {
    (1, 1, 1, 1, 1): "DECOLAR_POUSAR",
    (0, 0, 0, 0, 0): "PARAR_MOTOR",
    (1, 0, 0, 0, 0): "FRENTE",
    (1, 0, 0, 0, 1): "FLIP",
    (0, 1, 1, 0, 0): "TRAS"
}

def rodar_controle_gestos(drone):
    cap = cv2.VideoCapture(0)
    success, frame_inicial = cap.read()
    if not success:
        print("Não foi possível acessar a câmera do computador.")
        return

    altura, largura, _ = frame_inicial.shape
    p_time = 0
    decolado = False

    cv2.namedWindow("Modo Drone - Gestos", cv2.WINDOW_NORMAL)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img, resultados = processar_frame_mao(img)
        pontos_mao = coletar_coordenadas(resultados, largura, altura)
        
        comando_atual = "NENHUM GESTO DETECTADO"

        if len(pontos_mao) > 0:
            dedos = mapear_dedos_levantados(pontos_mao)
            chave_busca = tuple(dedos)
            
            if chave_busca in DICIONARIO_COMANDOS:
                comando_atual = DICIONARIO_COMANDOS[chave_busca]
                
                if drone:
                    try:
                        if comando_atual == "DECOLAR_POUSAR":
                            if not decolado:
                                drone.takeoff()
                                decolado = True
                            else:
                                drone.land()
                                decolado = False
                                
                        elif comando_atual == "PARAR_MOTOR":
                            drone.emergency()
                            decolado = False
                            
                        elif comando_atual == "FRENTE":
                            drone.move_forward(30)
                            
                        elif comando_atual == "TRAS":
                            drone.move_back(30)
                            
                        elif comando_atual == "FLIP":
                            drone.flip_forward()
                    except Exception as drone_error:
                        print(f"Erro ao enviar comando para o drone: {drone_error}")
            else:
                comando_atual = "GESTO DESCONHECIDO"

        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        bateria_status = f"BAT: {drone.get_battery()}%" if drone else "MODO: SIMULADOR"

        cv2.rectangle(img, (0, 0), (largura, 95), (40, 40, 40), cv2.FILLED)
        cv2.putText(img, f"COMANDO: {comando_atual} | {bateria_status}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, f"FPS: {int(fps)} | Pressione 'Q' para retornar ao Menu", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 230, 230), 1)

        cv2.imshow("Modo Drone - Gestos", img)
        
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or tecla == 27:
            break

    cap.release()
    cv2.destroyAllWindows()