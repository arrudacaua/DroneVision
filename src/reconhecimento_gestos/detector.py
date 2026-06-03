import cv2
import mediapipe as mp

# Inicialização global das ferramentas da biblioteca
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,  # Apenas uma mão é necessária para comandar o drone
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

def processar_frame_mao(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultados = hands.process(img_rgb)
    
    if resultados.multi_hand_landmarks:
        for hand_lms in resultados.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)
    
    return img, resultados

def coletar_coordenadas(resultados, largura, altura):
    pontos = []
    
    if resultados.multi_hand_landmarks:
        hand = resultados.multi_hand_landmarks[0]
        for i, lm in enumerate(hand.landmark):
            x = int(lm.x * largura)
            y = int(lm.y * altura)
            pontos.append((i, x, y))
    
    return pontos

def mapear_dedos_levantados(pontos):
    if not pontos:
        return []

    dedos = []
    
    if pontos[4][1] < pontos[3][1]:
        dedos.append(1)
    else:
        dedos.append(0)

    for ponta in [8, 12, 16, 20]:
        if pontos[ponta][2] < pontos[ponta - 2][2]:
            dedos.append(1)
        else:
            dedos.append(0)
    
    return dedos