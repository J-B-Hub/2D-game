class GameState:
    """Clase que maneja todo el estado del juego (puntuación, energía, etc.)"""
    
    def __init__(self, configuracion=None):
        self.configuracion = configuracion or {}
        
        # Estado del juego
        self.juego_corriendo = True
        self.juego_pausado = False
        self.juego_terminado = False
        self.mostrar_arbol = False
        
        # Posición y movimiento
        self.posicion_en_carretera = 0
        self.velocidad_carro = self.configuracion.get('car_speed', 3)
        
        # Estadísticas del jugador
        self.energia = self.configuracion.get('initial_energy', 100)
        self.energia_maxima = self.energia
        self.puntuacion = 0
        self.obstaculos_evitados = 0
        self.obstaculos_golpeados = set()
        
        # Control de tiempo
        self.contador_frames = 0
        self.tiempo_inicio = None
        # Salto (estadísticas)
        self.altura_actual_salto = 0
        self.saltos_realizados = 0
    
    def alternar_pausa(self):
        """Alterna entre pausado y no pausado"""
        if not self.juego_terminado:
            self.juego_pausado = not self.juego_pausado
    
    def alternar_mostrar_arbol(self):
        """Alterna la visualización del árbol"""
        self.mostrar_arbol = not self.mostrar_arbol
    
    def reiniciar(self):
        """Reinicia el estado del juego"""
        self.posicion_en_carretera = 0
        self.contador_frames = 0
        self.mostrar_arbol = False
        self.juego_pausado = False
        self.juego_terminado = False
        self.energia = self.energia_maxima
        self.puntuacion = 0
        self.obstaculos_evitados = 0
        self.obstaculos_golpeados = set()
        self.tiempo_inicio = None
        print("Estado del juego reiniciado")
    
    def actualizar_movimiento(self):
        """Actualiza la posición en la carretera"""
        if not self.juego_pausado and not self.juego_terminado:
            self.posicion_en_carretera += self.velocidad_carro
            self.puntuacion = int(self.posicion_en_carretera / 10)
    
    def reducir_energia(self, cantidad=20):
        """Reduce la energía del jugador"""
        self.energia -= cantidad
        if self.energia <= 0:
            self.energia = 0
            self.juego_terminado = True
    
    def agregar_obstaculo_golpeado(self, obstaculo, esta_saltando=False):
        """Registra un obstáculo como golpeado"""
        if obstaculo not in self.obstaculos_golpeados:
            self.obstaculos_golpeados.add(obstaculo)
            # Solo reducir energía si no está saltando
            if not esta_saltando:
                self.reducir_energia()
                print(f"¡Colisión con {obstaculo.obstacle_type}! Energía: {self.energia}")
            else:
                print(f"¡Colisión durante salto con {obstaculo.obstacle_type}! Sin pérdida de energía. Energía: {self.energia}")
    
    def contar_obstaculo_evitado(self):
        """Aumenta el contador de obstáculos evitados"""
        self.obstaculos_evitados += 1
    
    def incrementar_frames(self):
        """Incrementa el contador de frames"""
        self.contador_frames += 1
    
    def esta_activo(self):
        """Verifica si el juego está activo (no pausado ni terminado)"""
        return not self.juego_pausado and not self.juego_terminado
