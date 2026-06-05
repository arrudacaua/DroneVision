import sys
import os
import cv2
import time
import mediapipe as mp

# 🛠️ Força o Python a enxergar a estrutura de pastas a partir da raiz do projeto (Evita o erro de ModuleNotFoundError)
caminho_atual = os.path.dirname(os.path.abspath(__file__))
raiz_projeto = os.path.abspath(os.path.join(caminho_atual, "..", ".."))
if raiz_projeto not in sys.path:
    sys.path.append(raiz_projeto)

# Agora as importações funcionam apontando diretamente pelo caminho correto
from src.reconhecimento_gestos.detector import processar_frame_mao, coletar_coordenadas, mapear_dedos_levantados

# Configuração do Detector de Rosto do MediaPipe
mp_face = mp.solutions.face_detection
face_detection = mp_face.FaceDetection(min_detection_confidence=0.6)

DICIONARIO_COMANDOS = {
    (1, 1, 1, 1, 1): "DECOLAR_POUSAR",  # Mão aberta
    (0, 0, 0, 0, 0): "PARAR_MOTOR",     # Mão fechada
    (1, 0, 0, 0, 0): "FRENTE",          # Joinha
    (1, 0, 0, 0, 1): "FLIP",            # Hang Loose
    (0, 1, 1, 0, 0): "TRAS"             # Sinal de Paz (V)
}

def rodar_controle_gestos(drone=None):
    print("\n[INFO] Iniciando câmera para teste de gestos e face...")
    
    # Usando cv2.CAP_DSHOW para evitar travamentos de driver no Windows/Lenovo
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    # Se falhar o DirectShow, tenta o canal padrão
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    success, frame_inicial = cap.read()
    if not success or frame_inicial is None:
        print("\n⚠️ Erro: Não foi possível obter imagem da câmera.")
        print("💡 Verifique se a privacidade da câmera Lenovo (tecla F8) ou a trava física da lente não estão ativadas!")
        return

    altura, largura, _ = frame_inicial.shape
    p_time = 0
    decolado = False

    cv2.namedWindow("Modo Teste PC - Gestos e Face", cv2.WINDOW_NORMAL)

    while True:
        success, img = cap.read()
        if not success or img is None:
            break

        img = cv2.flip(img, 1) # Espelha a imagem para ficar natural
        
        # 1️⃣ DETECÇÃO DE ROSTO
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        resultados_face = face_detection.process(img_rgb)
        
        face_detectada = False
        centro_face_x = 0
        
        if resultados_face.detections:
            face_detectada = True
            deteccao = resultados_face.detections[0]
            bboxC = deteccao.location_data.relative_bounding_box
            
            face_x = int(bboxC.xmin * largura)
            face_y = int(bboxC.ymin * altura)
            face_w = int(bboxC.width * largura)
            face_h = int(bboxC.height * altura)
            centro_face_x = face_x + (face_w // 2)
            
            # Desenha o retângulo roxo ao redor do rosto
            cv2.rectangle(img, (face_x, face_y), (face_x + face_w, face_y + face_h), (255, 0, 255), 2)
            cv2.putText(img, "OPERADOR AUTORIZADO", (face_x, face_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        # 2️⃣ DEFINIÇÃO DA CAIXA VERDE (ZONA DE COMANDO)
        if face_detectada and centro_face_x > (largura // 2):
            box_x1, box_y1 = int(largura * 0.05), int(altura * 0.2)
            box_x2, box_y2 = int(largura * 0.45), int(altura * 0.8)
        else:
            box_x1, box_y1 = int(largura * 0.55), int(altura * 0.2)
            box_x2, box_y2 = int(largura * 0.95), int(altura * 0.8)

        cor_caixa = (0, 255, 0) if face_detectada else (0, 0, 255)
        cv2.rectangle(img, (box_x1, box_y1), (box_x2, box_y2), cor_caixa, 2)
        
        texto_status = "ZONA DE COMANDO ATIVA" if face_detectada else "AGUARDANDO ROSTO..."
        cv2.putText(img, texto_status, (box_x1, box_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cor_caixa, 2)

        # 3️⃣ PROCESSAMENTO DA MÃO
        img, resultados_mao = processar_frame_mao(img)
        pontos_mao = coletar_coordenadas(resultados_mao, largura, altura)
        
        comando_atual = "SISTEMA TRAVADO"

        if face_detectada and len(pontos_mao) > 0:
            mao_x = pontos_mao[9][1] # Ponto central da palma
            mao_y = pontos_mao[9][2]
            
            if box_x1 < mao_x < box_x2 and box_y1 < mao_y < box_y2:
                dedos = mapear_dedos_levantados(pontos_mao)
                chave_busca = tuple(dedos)
                
                if chave_busca in DICIONARIO_COMANDOS:
                    comando_atual = DICIONARIO_COMANDOS[chave_busca]
                    
                    # Caixa verde sólida preenchida para o texto (igual ao "Stop")
                    cv2.rectangle(img, (box_x1, box_y2 - 50), (box_x2, box_y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, comando_atual, (box_x1 + 20, box_y2 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

                    # Simulação de envio para o drone (só envia se o drone real existir)
                    if drone:
                        try:
                            if comando_atual == "DECOLAR_POUSAR":
                                if not decolado: drone.takeoff(); decolado = True
                                else: drone.land(); decolado = False
                            elif comando_atual == "FRENTE": drone.move_forward(30)
                            elif comando_atual == "TRAS": drone.move_back(30)
                        except Exception as d_err:
                            print(f"Erro drone: {d_err}")
                else:
                    comando_atual = "GESTO DESCONHECIDO"
            else:
                comando_atual = "COLOQUE A MAO NA CAIXA"
        elif len(pontos_mao) > 0 and not face_detectada:
            comando_atual = "ROSTO NAO DETECTADO"

        # HUD Superior do Menu de Testes
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        cv2.rectangle(img, (0, 0), (largura, 60), (40, 40, 40), cv2.FILLED)
        cv2.putText(img, f"STATUS: {comando_atual} | FPS: {int(fps)} | Pressione 'Q' para Sair", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        cv2.imshow("Modo Teste PC - Gestos e Face", img)
        
        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or tecla == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# 🚀 Execução Direta para Teste Isolado
if __name__ == "__main__":
    rodar_controle_gestos()