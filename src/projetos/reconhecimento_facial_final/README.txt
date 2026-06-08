PASSO A PASSO

1) Extraia esta pasta para um caminho simples, de preferencia:
   C:\Projetos\reconhecimento_facial_final

2) Coloque as fotos dentro da pasta rostos, seguindo o modelo:
   rostos\Rubens_Sousa\foto1.jpg
   rostos\Rubens_Sousa\foto2.jpg

3) Dê dois cliques em INSTALAR.bat.
   Ele cria a venv e instala as bibliotecas.

4) Depois dê dois cliques em RODAR.bat.

5) A webcam vai abrir. Para sair, aperte ESC.

COMANDOS MANUAIS, SE PREFERIR PELO TERMINAL:

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install dlib-bin
pip install -r requirements.txt --no-deps
pip install opencv-python numpy pillow click colorama
python reconhecimento_facial.py

OBSERVACOES:
- Use Python 3.11.
- Evite deixar o projeto em caminho com acento, tipo Área de Trabalho.
- Melhor caminho: C:\Projetos\reconhecimento_facial_final
- As pastas dentro de rostos viram os nomes exibidos na tela.
