import cv2
import time
import webbrowser

def rodar_scanner_qr(drone=None):
    print("\nIniciando câmera do computador para teste de QR Code...")
    
    cap = cv2.VideoCapture(0)
    
    success, frame_inicial = cap.read()
    if not success:
        print("⚠️ Não foi possível acessar a câmera do computador.")
        input("Pressione Enter para voltar ao menu...")
        return

    altura, largura, _ = frame_inicial.shape

    detector_qr = cv2.QRCodeDetector()
    p_time = 0
    ultimo_qr_lido = ""

    cv2.namedWindow("Modo Teste PC - Scanner QR", cv2.WINDOW_NORMAL)

    while True:
        success, img = cap.read()
        if not success:
            print("Erro ao capturar frame da webcam.")
            break

        img = cv2.flip(img, 1)

        dados, pontos, _ = detector_qr.detectAndDecode(img)

        conteudo_qr = "NENHUM QR CODE NA TELA"