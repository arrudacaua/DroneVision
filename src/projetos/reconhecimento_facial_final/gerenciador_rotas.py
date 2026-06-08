from djitellopy import Tello
import time

class ControladorDrone:
    def __init__(self):
        self.tello = Tello()
        self.tello.connect()
        self.historico_movimentos = []

    def executar_rota(self, comandos):
        print("Bateria inicial:", self.tello.get_battery(), "%")

        for acao, valor in comandos:
            if self.tello.get_battery() < 20:
                print("Bateria crítica! Abortando...")
                break
            
            print(f"Executando: {acao} {valor}")
            
            if acao == "takeoff":
                self.tello.takeoff()
            elif acao == "move_forward":
                self.tello.move_forward(valor)
                self.historico_movimentos.append(("move_back", valor))
            elif acao == "move_left":
                self.tello.move_left(valor)
                self.historico_movimentos.append(("move_right", valor))
            elif acao == "rotate_clockwise":
                self.tello.rotate_clockwise(valor)
                self.historico_movimentos.append(("rotate_counter_clockwise", valor))
            
            time.sleep(2) # Pausa para estabilização

# --- Execução ---
meu_drone = ControladorDrone()

# Rota para fazer um quadrado (ex: 50cm cada lado)
rota_quadrado = [
    ("takeoff",10),
    ("move_forward", 100),
    ("rotate_clockwise", 90),
    ("move_forward", 100),
    ("rotate_clockwise", 90),
    ("move_forward", 100),
    ("rotate_clockwise", 90),
    ("move_forward", 100),
    ("rotate_clockwise", 90)
]

meu_drone.executar_rota(rota_quadrado)
meu_drone.retornar_e_finalizar()
