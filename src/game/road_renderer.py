import pygame

class RoadRenderer:
    """Clase especializada en dibujar la carretera"""
    
    def __init__(self, ventana_width, ventana_height):
        # Configuración de la carretera
        self.altura_carretera = 200
        self.inicio_carretera_y = (ventana_height - self.altura_carretera) // 2
        self.fin_carretera_y = self.inicio_carretera_y + self.altura_carretera
        self.altura_carril = self.altura_carretera // 2
        self.ventana_width = ventana_width
    
    def dibujar_carretera(self, screen, posicion_en_carretera):
        """Dibuja la carretera completa con líneas y efectos"""
        # Fondo de carretera (gris oscuro)
        rectangulo_carretera = pygame.Rect(0, self.inicio_carretera_y, self.ventana_width, self.altura_carretera)
        pygame.draw.rect(screen, (64, 64, 64), rectangulo_carretera)
        
        # Bordes de carretera (líneas blancas)
        pygame.draw.line(screen, (255, 255, 255), 
                        (0, self.inicio_carretera_y), (self.ventana_width, self.inicio_carretera_y), 5)
        pygame.draw.line(screen, (255, 255, 255), 
                        (0, self.fin_carretera_y), (self.ventana_width, self.fin_carretera_y), 5)
        
        # Línea divisoria de carriles (línea amarilla discontinua)
        self.dibujar_linea_central(screen, posicion_en_carretera)
    
    def dibujar_linea_central(self, screen, posicion_en_carretera):
        """Dibuja la línea amarilla discontinua del centro"""
        centro_carretera = self.inicio_carretera_y + self.altura_carretera // 2
        
        for x in range(0, self.ventana_width, 40):
            if (x + posicion_en_carretera) % 80 < 20:  # Líneas discontinuas animadas
                pygame.draw.line(screen, (255, 255, 0), 
                               (x, centro_carretera), (x + 20, centro_carretera), 3)
    
    def obtener_posicion_carril_superior(self):
        """Devuelve la posición Y del carril superior"""
        return self.inicio_carretera_y + self.altura_carril // 2
    
    def obtener_posicion_carril_inferior(self):
        """Devuelve la posición Y del carril inferior"""
        return self.inicio_carretera_y + self.altura_carril + self.altura_carril // 2
