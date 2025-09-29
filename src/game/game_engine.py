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
        
        # Meta del juego
        self.distancia_meta = configuracion.get('meta_distance', 10000)  # Distancia para ganar (valor predeterminado)
        self.victoria = False  # Nuevo estado para indicar que se ha ganado el juego
    
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
        # Controles que funcionan SIEMPRE (incluso en pausa)
        if self.input_manager.quiere_pausar():
            self.estado_juego.alternar_pausa()
        
        if self.input_manager.quiere_reiniciar():
            self.reiniciar_juego()
        
        if self.input_manager.quiere_mostrar_arbol():
            self.modo_avl_en_vivo = not self.modo_avl_en_vivo
            print("AVL overlay", "ON" if self.modo_avl_en_vivo else "OFF")
        
        # AGREGAR OBSTÁCULOS FUNCIONA INCLUSO EN PAUSA
        if self.input_manager.quiere_agregar_obstaculo():
            self.gestor_obstaculos.crear_obstaculo_aleatorio(self.estado_juego.posicion_en_carretera)
            estado_texto = "PAUSADO" if self.estado_juego.juego_pausado else "ACTIVO"
            print(f"Obstáculo agregado mientras el juego está {estado_texto}")

        # DEBUG Y VERIFICACIÓN FUNCIONAN SIEMPRE
        if self.input_manager.quiere_verificar_balance():
            self.verificar_balance_avl()

        if self.input_manager.quiere_debug():
            # Contar nodos
            def _contar(n):
                if not n: return 0
                return 1 + _contar(n.left) + _contar(n.right)
            total = _contar(self.gestor_obstaculos.arbol.root)
            estado_texto = "PAUSADO" if self.estado_juego.juego_pausado else "ACTIVO"
            print(f"[DEBUG] Juego {estado_texto} - AVL activo={self.modo_avl_en_vivo} nodos={total}")
        
        # Controles de juego (solo si el juego está ACTIVO)
        if self.estado_juego.esta_activo():
            if self.input_manager.quiere_saltar():
                self.carro.iniciar_salto(self.carro_y)
                self.estado_juego.saltos_realizados += 1

            if self.input_manager.quiere_mover_arriba():
                self.carro_y = self.game_renderer.obtener_posicion_carril_superior()
            
            if self.input_manager.quiere_mover_abajo():
                self.carro_y = self.game_renderer.obtener_posicion_carril_inferior()
    
    def actualizar_logica_juego(self):
        """Actualiza la lógica principal del juego"""
        # Mover el carro hacia adelante
        self.estado_juego.actualizar_movimiento()
        
        # Verificar si se alcanzó la meta
        if self.estado_juego.posicion_en_carretera >= self.distancia_meta:
            self.victoria = True
            self.estado_juego.juego_pausado = True  # Pausar el juego al ganar
            return
        
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
        if self.victoria:
            self.mostrar_pantalla_victoria()
            return
            
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
        
        # Mostrar información de la meta
        self.dibujar_info_meta()
    
    def dibujar_info_meta(self):
        """Muestra información sobre la meta y el progreso"""
        progreso = min(self.estado_juego.posicion_en_carretera / self.distancia_meta, 1.0)
        porcentaje = int(progreso * 100)
        
        # Dibujar barra de progreso
        ancho_barra = 200
        alto_barra = 20
        x_barra = self.ventana.width - ancho_barra - 20
        y_barra = 20
        
        # Fondo de la barra
        pygame.draw.rect(self.ventana.screen, (50, 50, 50), (x_barra, y_barra, ancho_barra, alto_barra))
        # Progreso
        pygame.draw.rect(self.ventana.screen, (0, 255, 0), 
                        (x_barra, y_barra, int(ancho_barra * progreso), alto_barra))
        
        # Texto de progreso
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(f"Meta: {porcentaje}%", True, (255, 255, 255))
        texto_rect = texto.get_rect(midleft=(x_barra - 10, y_barra + alto_barra//2))
        self.ventana.screen.blit(texto, texto_rect)
        
        # Distancia restante
        distancia_restante = max(0, self.distancia_meta - self.estado_juego.posicion_en_carretera)
        texto_distancia = fuente.render(f"Faltan: {distancia_restante:.0f} m", True, (255, 255, 255))
        texto_dist_rect = texto_distancia.get_rect(topleft=(x_barra, y_barra + alto_barra + 5))
        self.ventana.screen.blit(texto_distancia, texto_dist_rect)
    
    def mostrar_pantalla_victoria(self):
        """Muestra la pantalla de victoria"""
        # Limpiar pantalla
        self.ventana.clear()
        
        # Dibujar título
        fuente_titulo = pygame.font.Font(None, 64)
        texto_titulo = fuente_titulo.render("¡VICTORIA!", True, (255, 255, 0))
        titulo_rect = texto_titulo.get_rect(center=(self.ventana.width//2, self.ventana.height//2 - 100))
        self.ventana.screen.blit(texto_titulo, titulo_rect)
        
        # Dibujar estadísticas
        fuente_stats = pygame.font.Font(None, 32)
        
        texto_distancia = fuente_stats.render(
            f"Distancia recorrida: {self.estado_juego.posicion_en_carretera:.0f} m", 
            True, (200, 200, 200))
        dist_rect = texto_distancia.get_rect(center=(self.ventana.width//2, self.ventana.height//2))
        self.ventana.screen.blit(texto_distancia, dist_rect)
        
        texto_saltos = fuente_stats.render(
            f"Saltos realizados: {self.estado_juego.saltos_realizados}", 
            True, (200, 200, 200))
        saltos_rect = texto_saltos.get_rect(center=(self.ventana.width//2, self.ventana.height//2 + 40))
        self.ventana.screen.blit(texto_saltos, saltos_rect)
        
        # Revisar si el atributo existe antes de mostrarlo
        if hasattr(self.estado_juego, 'colisiones_evitadas'):
            texto_colisiones = fuente_stats.render(
                f"Colisiones evitadas: {self.estado_juego.colisiones_evitadas}", 
                True, (200, 200, 200))
            colisiones_rect = texto_colisiones.get_rect(center=(self.ventana.width//2, self.ventana.height//2 + 80))
            self.ventana.screen.blit(texto_colisiones, colisiones_rect)
        
        # Dibujar instrucciones
        fuente_instr = pygame.font.Font(None, 28)
        texto_instr = fuente_instr.render("Presiona R para reiniciar - ESC para salir", True, (150, 150, 150))
        instr_rect = texto_instr.get_rect(center=(self.ventana.width//2, self.ventana.height//2 + 140))
        self.ventana.screen.blit(texto_instr, instr_rect)
        
        # Actualizar pantalla
        self.ventana.update()
        
        # Verificar si se quiere reiniciar
        if self.input_manager.quiere_reiniciar():
            self.reiniciar_juego()
        
        # Verificar si se quiere salir
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.estado_juego.juego_corriendo = False
    
    def reiniciar_juego(self):
        """Reinicia el juego completo"""
        # Reiniciar estado
        self.estado_juego.reiniciar()
        
        # Reiniciar posición del carro
        self.carro_x = 50
        self.carro_y = self.game_renderer.obtener_posicion_carril_superior()
        
        # Reiniciar obstáculos
        self.gestor_obstaculos.reiniciar_obstaculos()
        
        # Reiniciar estado de victoria
        self.victoria = False
    
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
