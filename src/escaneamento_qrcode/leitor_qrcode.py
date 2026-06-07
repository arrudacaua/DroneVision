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
        if dados:
            conteudo_qr = dados.strip()

            if pontos is not None:
                pontos = pontos.astype(int)
                for i in range(len(pontos[0])):
                    ponto_atual = tuple(pontos[0][i])
                    proximo_ponto = tuple(pontos[0][(i + 1) % len(pontos[0])])
                    cv2.line(img, ponto_atual, proximo_ponto, (0, 255, 0), 3)

            if conteudo_qr.startswith("http") and conteudo_qr != ultimo_qr_lido:
                print(f"\n🌐 Link identificado! Abrindo no navegador: {conteudo_qr}")
                
                webbrowser.open(conteudo_qr)
                
                ultimo_qr_lido = conteudo_qr

        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        cv2.rectangle(img, (0, 0), (largura, 95), (40, 40, 40), cv2.FILLED)
        cv2.putText(img, f"QR CODE: {conteudo_qr}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(img, f"FPS: {int(fps)} | MODO: TESTE PC | Pressione 'Q' para Sair", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 230, 230), 1)

        cv2.imshow("Modo Teste PC - Scanner QR", img)

        tecla = cv2.waitKey(1) & 0xFF
        if tecla == ord('q') or tecla == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
