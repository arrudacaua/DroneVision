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
                print("Bateria crítica! Abortando rota para segurança...")
                break
            
            print(f"Executando: {acao} {valor}")
            
            if acao == "takeoff":
                self.tello.takeoff()
                # Não adicionamos o takeoff no histórico de retorno 
                # porque faremos um 'land' direto no final.
            elif acao == "move_forward":
                self.tello.move_forward(valor)
                self.historico_movimentos.append(("move_back", valor))
            elif acao == "move_left":
                self.tello.move_left(valor)
                self.historico_movimentos.append(("move_right", valor))
            elif acao == "rotate_clockwise":
                self.tello.rotate_clockwise(valor)
                self.historico_movimentos.append(("rotate_counter_clockwise", valor))
            
            time.sleep(1) # Pausa curta opcional para estabilização

    def retornar_e_finalizar(self):
        print("\n--- Iniciando rota de retorno baseada no histórico ---")
        
        # Inverte o histórico para fazer o caminho inverso (da última ação para a primeira)
        for acao, valor in reversed(self.historico_movimentos):
            if self.tello.get_battery() < 10:
                print("Bateria perigosamente baixa! Forçando pouso imediato.")
                break
                
            print(f"Desfazendo movimento: {acao} {valor}")
            
            if acao == "move_back":
                self.tello.move_back(valor)
            elif acao == "move_right":
                self.tello.move_right(valor)
            elif acao == "rotate_counter_clockwise":
                self.tello.rotate_counter_clockwise(valor)
            
            time.sleep(1)
            
        print("Pousando em segurança...")
        self.tello.land()


# --- Execução ---
meu_drone = ControladorDrone()

# Rota para fazer um quadrado (valores em centímetros e graus)
# Nota: Removi o valor '10' do takeoff pois a função não o utiliza
rota_quadrado = [
    ("takeoff", 0), 
    ("move_forward", 100),
    ("rotate_clockwise", 90),
    ("move_forward", 100),
    ("rotate_clockwise", 90),
    ("move_forward", 100),
    ("rotate_clockwise", 90),
    ("move_forward", 100),
    ("rotate_clockwise", 90)
]

# Executa a rota do quadrado
meu_drone.executar_rota(rota_quadrado)

# Executa o retorno baseado no que ele andou e depois pousa
meu_drone.retornar_e_finalizar()