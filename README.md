# DroneVision

DroneVision é um sistema modular de visão computacional desenvolvido como projeto de primeiro período de faculdade. O objetivo principal do ecossistema é atuar como uma interface inteligente de controle para drones (focando na biblioteca djitellopy), traduzindo dados visuais capturados por uma câmera em comandos de navegação em tempo real.

O diferencial do projeto está na sua arquitetura estruturada. Em vez de concentrar toda a lógica em um único script, o sistema foi modularizado em pacotes independentes coordenados por um menu central. Essa abordagem garante manutenibilidade e otimização do processamento, carregando módulos pesados de inteligência artificial apenas quando requisitados pelo usuário.

## Estrutura do Projeto

O software é dividido em módulos especializados dentro do diretório principal:

* src/main.py: O orquestrador central do sistema. Gerencia a interface de texto com o usuário e gerencia a inicialização e o encerramento seguro dos módulos.
* src/gestos/: Módulo focado no mapeamento anatômico da mão humana utilizando MediaPipe. É composto por um detector puro que processa coordenadas geométricas (X, Y) e um tradutor que converte combinações de dedos levantados em comandos operacionais como decolagem, pouso e direções.
* src/reconhecimento/: Diretório reservado para os algoritmos de identificação e rastreamento facial.
* src/qrcode/: Módulo encarregado da leitura e decodificação de tags em tempo real para automação de tarefas.
* src/rotas/: Módulo de telemetria para planejamento de caminhos coordenados e monitoramento do status do drone.

## Funcionalidades do Módulo de Gestos

O sistema traduz interações físicas em strings de comando através do monitoramento de marcos anatômicos. As leituras geométricas realizam as seguintes conversões diretas:

* Mão totalmente aberta: Comando de decolagem ou pouso.
* Mão totalmente fechada: Parada de emergência dos motores.
* Gesto de polegar levantado (Joinha): Movimentação para frente.
* Gesto com polegar e mínimo levantados (Hang Loose): Comando para execução de manobra acrobática (Flip).
* Indicador e médio levantados: Movimentação para trás.

## Requisitos de Sistema

A execução do ambiente exige uma versão estável do interpretador Python (ambiente homologado nas versões 3.11 ou 3.12). Os pacotes fundamentais utilizados são:

* OpenCV (opencv-python)
* MediaPipe
* DJITelloPy

## Instruções de Instalação e Execução

Para configurar o ambiente virtual local e instalar as dependências necessárias sem interferir nas configurações globais do sistema, siga as instruções abaixo pelo terminal do seu ambiente de desenvolvimento.

1. Clone o repositório para sua máquina local:
   git clone https://github.com/seu-usuario/DroneVision.git
   cd DroneVision

2. Crie e ative o ambiente virtual isolado (Virtual Environment):
   python -m venv .venv
   
   No Windows (PowerShell):
   .venv/Scripts/Activate.ps1
   
   No Linux ou macOS:
   source .venv/bin/activate

3. Instale as dependências listadas no arquivo de requisitos:
   pip install -r requirements.txt

4. Inicie a aplicação através do orquestrador principal:
   python src/main.py