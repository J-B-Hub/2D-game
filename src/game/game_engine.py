import pygame
from .input_manager import InputManager
from .game_state import GameState
from .collision_detector import CollisionDetector
from .game_renderer import GameRenderer
from data_structures.avl_visualizer import AVLVisualizer

class GameEngineModular:
    """Motor del juego modular - cada responsabilidad en su propia clase"""
    
    def __init__(self, carro, gestor_obstaculos, ventana, configuracion=None):
        # Referencias principales
        self.carro = carro
        self.gestor_obstaculos = gestor_obstaculos
        self.ventana = ventana
        
        # Módulos especializados
        self.input_manager = InputManager()
        self.estado_juego = GameState(configuracion)
        self.collision_detector = CollisionDetector()
        self.game_renderer = GameRenderer(ventana)
        self.avl_visualizer = AVLVisualizer()  # Instancia del visualizador, aquí creamos el visualizador del árbol
        
        # Posición del carrito
        self.carro_x = 50  # Posición fija en pantalla El carrito siempre arranca en el borde izquierdo
        self.carro_y = self.game_renderer.obtener_posicion_carril_superior()
    
    def actualizar(self):
        """Actualiza la lógica del juego - versión simplificada"""
        # Incrementar contador de frames
        self.estado_juego.incrementar_frames()
        
        # Actualizar entradas
        self.input_manager.actualizar_entradas(self.estado_juego.contador_frames)
        
        # Manejar entradas del jugador
        self.manejar_entradas()
        
        # Si el juego está activo, actualizar lógica
        if self.estado_juego.esta_activo():
            self.actualizar_logica_juego()
    
    def manejar_entradas(self):
        """Maneja todas las entradas del jugador"""
        # Controles de juego; pausa, reinicio, mostrar árbol, agregar obstáculo
        if self.input_manager.quiere_pausar():
            self.estado_juego.alternar_pausa()
        
        if self.input_manager.quiere_reiniciar():
            self.reiniciar_juego()
        
        if self.input_manager.quiere_mostrar_arbol():
            print("¡Se presionó la T!")
            self.game_renderer.ui_renderer.dibujar_visualizacion_arbol(self.gestor_obstaculos.arbol.root)
        
        if self.input_manager.quiere_agregar_obstaculo():
            self.gestor_obstaculos.crear_obstaculo_aleatorio(self.estado_juego.posicion_en_carretera)
        
        # Movimiento del carro (solo si el juego está activo)
        if self.estado_juego.esta_activo():
            if self.input_manager.quiere_mover_arriba():
                self.carro_y = self.game_renderer.obtener_posicion_carril_superior()
            
            if self.input_manager.quiere_mover_abajo():
                self.carro_y = self.game_renderer.obtener_posicion_carril_inferior()
    
    def actualizar_logica_juego(self):
        """Actualiza la lógica principal del juego"""
        # Mover el carro hacia adelante
        self.estado_juego.actualizar_movimiento()
        
        # Obtener obstáculos visibles
        obstaculos_visibles = self.gestor_obstaculos.obtener_obstaculos_visibles(
            self.estado_juego.posicion_en_carretera
        )
        
        # Verificar colisiones
        self.collision_detector.verificar_colisiones(
            self.carro_x, self.carro_y, obstaculos_visibles,
            self.estado_juego.posicion_en_carretera, self.estado_juego
        )
        
        # Limpiar obstáculos pasados
        self.gestor_obstaculos.eliminar_obstaculos_pasados(self.estado_juego.posicion_en_carretera)
    
    def dibujar(self):
        """Dibuja todo el juego"""
        # Obtener obstáculos visibles
        obstaculos_visibles = self.gestor_obstaculos.obtener_obstaculos_visibles(
            self.estado_juego.posicion_en_carretera
        )
        
        # Delegar todo el renderizado al GameRenderer
        self.game_renderer.dibujar_todo(
            self.estado_juego, self.carro_x, self.carro_y,
            obstaculos_visibles, self.estado_juego.posicion_en_carretera,
            self.gestor_obstaculos
        )
    
    def reiniciar_juego(self):
        """Reinicia el juego completo"""
        # Reiniciar estado
        self.estado_juego.reiniciar()
        
        # Reiniciar posición del carro
        self.carro_x = 50
        self.carro_y = self.game_renderer.obtener_posicion_carril_superior()
        
        # Reiniciar obstáculos
        self.gestor_obstaculos.reiniciar_obstaculos()
    
    def ejecutar(self):
        """Bucle principal del juego - simplificado"""
        reloj = pygame.time.Clock()
        
        while self.estado_juego.juego_corriendo:
            # Manejar eventos de cierre
            # Aquí revisamos si el jugador cerró la ventana
            evento_salir = self.ventana.handle_events()
            if evento_salir:
                break

            # ---PARCE ESTO ES LO NUEVO: Captura eventos de teclado para mostrar el árbol---
            # ---Aquí es donde capturamos la tecla T ---
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        print("¡Se presionó la T!")
                        print("Raíz del árbol:", self.gestor_obstaculos.avl_root)
                        # Muestra el árbol usando pyplot
                        # Cuando el jugador presiona la T, mostramos el árbol AVL en una ventana aparte
                        # Eso es lo que le gusta al profe, que se vea el arbolito bien bonito
                        self.ui_renderer.dibujar_visualizacion_arbol(self.gestor_obstaculos.avl_root)
            # ---------------------------------------------------------------

            # Actualizar lógica
            self.actualizar()
            
            # Dibujar todo
            self.dibujar()
            
            # Mantener 60 FPS
            # Pa' que corra a 60 FPS, ni muy rápido ni muy lento
            reloj.tick(60)
