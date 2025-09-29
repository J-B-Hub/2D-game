import pygame
from .road_renderer import RoadRenderer
from .ui_renderer import UIRenderer
from .avl_overlay_renderer import AVLMiniRenderer

class GameRenderer:
    """Clase que coordina todo el renderizado del juego"""
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.road_renderer = RoadRenderer(ventana.width, ventana.height)
        self.ui_renderer = UIRenderer(ventana.width, ventana.height)
        self.avl_overlay = AVLMiniRenderer(ventana.width, ventana.height)
    
    def dibujar_todo(self, estado_juego, carro, carro_x, carro_y, obstaculos_visibles, posicion_en_carretera, gestor_obstaculos, mostrar_avl=False):
        """Dibuja todos los elementos del juego"""
        # Fondo cielo degradado
        screen = self.ventana.screen
        import pygame
        for y in range(self.ventana.height):
            t = y / self.ventana.height
            r = int(30 + 40 * t)
            g = int(120 + 80 * t)
            b = int(200 + 40 * t)
            pygame.draw.line(screen, (r,g,b), (0,y), (self.ventana.width,y))
    
        # Dibujar carretera
        self.road_renderer.dibujar_carretera(self.ventana.screen, posicion_en_carretera)
    
        # Dibujar carro (si tiene sprite usarlo)
        if hasattr(carro, 'render') and getattr(carro, 'sprite', None) is not None:
            carro.render(self.ventana, carro_x, carro_y)
        else:
            self.dibujar_carro(carro_x, carro_y)
    
        # Dibujar obstáculos
        self.dibujar_obstaculos(obstaculos_visibles, posicion_en_carretera, carro_x)
    
        # Dibujar interfaz
        self.ui_renderer.dibujar_barra_energia(self.ventana.screen, estado_juego.energia, estado_juego.energia_maxima)
        self.ui_renderer.dibujar_estadisticas(
            self.ventana.screen,
            estado_juego.puntuacion,
            estado_juego.obstaculos_evitados,
            estado_juego.energia
        )
        self.ui_renderer.dibujar_instrucciones(self.ventana.screen)
    
        # Ya NO se dibuja el árbol AVL aquí, solo se dibuja cuando el usuario presiona T en el motor principal.
        # Elimina la llamada a dibujar_visualizacion_arbol aquí para evitar errores.
    
        # Dibujar pantallas especiales
        if estado_juego.juego_pausado:
            self.ui_renderer.dibujar_pantalla_pausa(self.ventana.screen)
        elif estado_juego.juego_terminado:
            self.ui_renderer.dibujar_pantalla_game_over(self.ventana.screen, estado_juego.puntuacion)
    
        # Actualizar pantalla
        # Overlay AVL (en tiempo real) si está activo
        if mostrar_avl:
            try:
                arbol_root = gestor_obstaculos.arbol.root
                # Debug: contar nodos
                def _contar(n):
                    if not n: return 0
                    return 1 + _contar(n.left) + _contar(n.right)
                total = _contar(arbol_root)
                # Solo imprimir ocasionalmente (puntuacion divisible por 60)
                if estado_juego.contador_frames % 120 == 0:
                    print(f"[AVL Overlay] Dibujando {total} nodos")
                self.avl_overlay.dibujar(self.ventana.screen, arbol_root)
            except Exception as e:
                # Evitar que falle el juego por error de overlay
                print("Error dibujando overlay AVL:", e)

        self.ventana.update()
    
    def dibujar_carro(self, carro_x, carro_y):
        """Dibuja el carro del jugador"""
        rectangulo_carro = pygame.Rect(carro_x, carro_y, 50, 50)
        self.ventana.draw_car(rectangulo_carro)
    
    def dibujar_obstaculos(self, obstaculos_visibles, posicion_en_carretera, carro_x):
        """Dibuja todos los obstáculos visibles"""
        for obstaculo in obstaculos_visibles:
            # Calcular posición en pantalla
            x_pantalla = obstaculo.x - posicion_en_carretera + carro_x
            
            # Solo dibujar si está visible en pantalla
            if -50 <= x_pantalla <= self.ventana.width + 50:
                rectangulo_obstaculo = pygame.Rect(x_pantalla, obstaculo.y, obstaculo.width, obstaculo.height)
                obstaculo.render(self.ventana.screen, custom_rect=rectangulo_obstaculo)
    
    def obtener_posicion_carril_superior(self):
        """Obtiene la posición Y del carril superior"""
        return self.road_renderer.obtener_posicion_carril_superior()
    
    def obtener_posicion_carril_inferior(self):
        """Obtiene la posición Y del carril inferior"""
        return self.road_renderer.obtener_posicion_carril_inferior()
