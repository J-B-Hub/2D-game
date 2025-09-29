import pygame
from .input_manager import InputManager
from .game_state import GameState
from .collision_detector import CollisionDetector
from .game_renderer import GameRenderer
import time

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
        # AVL vivo (overlay interno)
        self.modo_avl_en_vivo = True  # Mostrar overlay AVL desde el inicio
        # Salto
        self._ultimo_tiempo = time.time()
        self.desplazamiento_vertical_actual = 0
        
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
            self.modo_avl_en_vivo = not self.modo_avl_en_vivo
            print("AVL overlay", "ON" if self.modo_avl_en_vivo else "OFF")
        
        if self.input_manager.quiere_agregar_obstaculo():
            self.gestor_obstaculos.crear_obstaculo_aleatorio(self.estado_juego.posicion_en_carretera)

        if self.input_manager.quiere_saltar():
            self.carro.iniciar_salto(self.carro_y)
            self.estado_juego.saltos_realizados += 1

        if self.input_manager.quiere_verificar_balance():
            self.verificar_balance_avl()

        if self.input_manager.quiere_debug():
            # Contar nodos
            def _contar(n):
                if not n: return 0
                return 1 + _contar(n.left) + _contar(n.right)
            total = _contar(self.gestor_obstaculos.arbol.root)
            print(f"[DEBUG] AVL activo={self.modo_avl_en_vivo} nodos={total}")
        
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
        
        # Actualizar salto
        ahora = time.time()
        dt = ahora - self._ultimo_tiempo
        self._ultimo_tiempo = ahora
        self.desplazamiento_vertical_actual = self.carro.actualizar_salto(dt, self.carro_y)
        self.estado_juego.altura_actual_salto = -self.desplazamiento_vertical_actual

        # Obtener obstáculos visibles
        obstaculos_visibles = self.gestor_obstaculos.obtener_obstaculos_visibles(
            self.estado_juego.posicion_en_carretera
        )
        
        # Verificar colisiones
        self.collision_detector.verificar_colisiones(
            self.carro_x, self.carro_y, obstaculos_visibles,
            self.estado_juego.posicion_en_carretera, self.estado_juego,
            desplazamiento_vertical=self.desplazamiento_vertical_actual,
            esta_saltando=self.carro.esta_saltando
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
        y_render = self.carro_y + self.desplazamiento_vertical_actual
        self.game_renderer.dibujar_todo(
            self.estado_juego, self.carro, self.carro_x, y_render,
            obstaculos_visibles, self.estado_juego.posicion_en_carretera,
            self.gestor_obstaculos, mostrar_avl=self.modo_avl_en_vivo
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.estado_juego.juego_corriendo = False
            self.ventana.handle_events()

            # Actualizar lógica
            self.actualizar()
            
            # Dibujar todo
            self.dibujar()
            
            # Mantener 60 FPS
            # Pa' que corra a 60 FPS, ni muy rápido ni muy lento
            reloj.tick(60)

    # Nada que cerrar ahora que el overlay es interno

    # --- AVL vivo y balance ---
    # (El código de hilos para matplotlib fue removido; ahora el árbol se dibuja en overlay)

    def verificar_balance_avl(self):
        raiz = self.gestor_obstaculos.arbol.root
        if not raiz:
            print("AVL vacío")
            return
        desbalance = []
        def dfs(n):
            if not n: return 0
            hl = dfs(n.left)
            hr = dfs(n.right)
            bal = hl - hr
            if abs(bal) > 1:
                desbalance.append((getattr(n,'x_position',None), bal))
            return max(hl, hr) + 1
        dfs(raiz)
        if desbalance:
            print("Nodos desbalanceados:", desbalance)
        else:
            print("AVL OK")
