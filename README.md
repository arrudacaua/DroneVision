# DroneVision

DroneVision é um sistema modular de visão computacional desenvolvido como projeto acadêmico com foco em automação, monitoramento e controle de drones utilizando Python.

O projeto integra técnicas de Visão Computacional, Reconhecimento Facial, Leitura de QR Code e Planejamento de Rotas para o drone DJI Tello, utilizando a biblioteca DJITelloPy.

Diferentemente da primeira versão do projeto, os módulos foram desacoplados e podem ser executados individualmente, permitindo maior flexibilidade para testes, manutenção e desenvolvimento.

---

# Estrutura do Projeto

O sistema está organizado em módulos independentes:

* `reconhecimento_facial.py`
  Responsável pelo reconhecimento facial em tempo real utilizando OpenCV e Face Recognition.

* `leitor_qrcode.py`
  Responsável pela leitura e interpretação de QR Codes através da câmera.

* `gerenciador_rotas.py`
  Responsável pela criação e gerenciamento de rotas de navegação.

* `executor_rotas.py`
  Responsável pela execução das rotas previamente definidas no drone.

* `rostos/`
  Diretório que armazena as imagens utilizadas para cadastro facial.

---

# Funcionalidades

## Reconhecimento Facial

* Cadastro de múltiplos usuários.
* Identificação facial em tempo real.
* Exibição do nome do usuário detectado.
* Suporte para imagens JPG, JPEG e PNG.

## Leitura de QR Code

* Detecção automática de QR Codes.
* Leitura em tempo real pela câmera.
* Possibilidade de utilização para automação de comandos.

## Gerenciamento de Rotas

* Criação de sequências de movimentação.
* Organização de comandos de navegação.
* Estrutura preparada para integração com drones.

## Controle do Drone

* Integração com a biblioteca DJITelloPy.
* Comunicação com o drone DJI Tello.
* Execução de comandos de movimentação.
* Monitoramento básico de bateria.

---

# Requisitos

O projeto foi desenvolvido utilizando:

* Python 3.11+
* OpenCV
* Face Recognition
* NumPy
* DJITelloPy
* Pillow

---

# Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/DroneVision.git
cd DroneVision
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Execução dos Módulos

Os módulos são executados individualmente.

### Reconhecimento Facial

```bash
python reconhecimento_facial.py
```

### Leitor de QR Code

```bash
python leitor_qrcode.py
```

### Gerenciador de Rotas

```bash
python gerenciador_rotas.py
```

### Executor de Rotas

```bash
python executor_rotas.py
```

---

# Cadastro de Rostos

As imagens devem ser organizadas da seguinte forma:

```text
rostos/
├── Camillo_Carvalho/
│   ├── foto1.jpg
│   ├── foto2.jpg
│
├── Joao_Paulo/
│   ├── foto1.jpg
│
├── Rubens_Sousa/
│   ├── foto1.jpg
```

Cada pasta representa uma pessoa e pode conter várias imagens para melhorar a precisão do reconhecimento.

---

# Tecnologias Utilizadas

* Python
* OpenCV
* Face Recognition
* NumPy
* DJITelloPy
* QRCode
* Git
* GitHub

---

# Autor

Projeto desenvolvido para a disciplina DroneVision como atividade acadêmica de graduação.
