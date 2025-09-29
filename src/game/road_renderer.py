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
        """Dibuja la carretera completa con degradados y efectos"""
        # Degradado vertical simple
        for i in range(self.altura_carretera):
            t = i / self.altura_carretera
            # Interpolar gris oscuro a gris medio
            c = int(40 + 40 * t)
            pygame.draw.line(screen, (c, c, c), (0, self.inicio_carretera_y + i), (self.ventana_width, self.inicio_carretera_y + i))

        # Bordes con sombra ligera
        sombra_color = (20, 20, 20)
        pygame.draw.rect(screen, sombra_color, (0, self.inicio_carretera_y, self.ventana_width, 4))
        pygame.draw.rect(screen, sombra_color, (0, self.fin_carretera_y - 4, self.ventana_width, 4))
        
        # Bordes externos brillantes
        pygame.draw.line(screen, (235, 235, 235), (0, self.inicio_carretera_y), (self.ventana_width, self.inicio_carretera_y), 2)
        pygame.draw.line(screen, (235, 235, 235), (0, self.fin_carretera_y), (self.ventana_width, self.fin_carretera_y), 2)

        # Textura pseudo-asfalto (píxeles esporádicos)
        import random
        for _ in range(120):
            x = random.randint(0, self.ventana_width-1)
            y = random.randint(self.inicio_carretera_y, self.fin_carretera_y-1)
            if (x + y + posicion_en_carretera) % 17 == 0:
                screen.set_at((x, y), (90, 90, 90))

        # Línea central estilizada
        self.dibujar_linea_central(screen, posicion_en_carretera)
    
    def dibujar_linea_central(self, screen, posicion_en_carretera):
        """Dibuja la línea amarilla discontinua del centro con brillo"""
        centro = self.inicio_carretera_y + self.altura_carretera // 2
        import math
        for x in range(0, self.ventana_width, 40):
            fase = (x + posicion_en_carretera) % 80
            if fase < 28:
                # Brillo respirando
                intensidad = 200 + int(55 * math.sin((posicion_en_carretera + x) * 0.01))
                color = (255, intensidad, 0)
                pygame.draw.line(screen, color, (x, centro), (x + 26, centro), 4)
    
    def obtener_posicion_carril_superior(self):
        """Devuelve la posición Y del carril superior"""
        return self.inicio_carretera_y + self.altura_carril // 2
    
    def obtener_posicion_carril_inferior(self):
        """Devuelve la posición Y del carril inferior"""
        return self.inicio_carretera_y + self.altura_carril + self.altura_carril // 2
