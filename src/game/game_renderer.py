import pygame
from .road_renderer import RoadRenderer
from .ui_renderer import UIRenderer

class GameRenderer:
    """Clase que coordina todo el renderizado del juego"""
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.road_renderer = RoadRenderer(ventana.width, ventana.height)
        self.ui_renderer = UIRenderer(ventana.width, ventana.height)
    
    def dibujar_todo(self, estado_juego, carro_x, carro_y, obstaculos_visibles, posicion_en_carretera, gestor_obstaculos):
        """Dibuja todos los elementos del juego"""
        # Limpiar pantalla
        self.ventana.clear()
    
        # Dibujar carretera
        self.road_renderer.dibujar_carretera(self.ventana.screen, posicion_en_carretera)
    
        # Dibujar carro
        self.dibujar_carro(carro_x, carro_y)
    
        # Dibujar obstáculos
        self.dibujar_obstaculos(obstaculos_visibles, posicion_en_carretera, carro_x)
    
        # Dibujar interfaz
        self.ui_renderer.dibujar_barra_energia(self.ventana.screen, estado_juego.energia, estado_juego.energia_maxima)
        self.ui_renderer.dibujar_estadisticas(self.ventana.screen, estado_juego.puntuacion, 
                                         estado_juego.obstaculos_evitados, estado_juego.energia)
        self.ui_renderer.dibujar_instrucciones(self.ventana.screen)
    
        # Ya NO se dibuja el árbol AVL aquí, solo se dibuja cuando el usuario presiona T en el motor principal.
        # Elimina la llamada a dibujar_visualizacion_arbol aquí para evitar errores.
    
        # Dibujar pantallas especiales
        if estado_juego.juego_pausado:
            self.ui_renderer.dibujar_pantalla_pausa(self.ventana.screen)
        elif estado_juego.juego_terminado:
            self.ui_renderer.dibujar_pantalla_game_over(self.ventana.screen, estado_juego.puntuacion)
    
        # Actualizar pantalla
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
