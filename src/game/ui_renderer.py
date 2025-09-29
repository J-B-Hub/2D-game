import pygame
from data_structures.avl_visualizer import AVLVisualizer
class UIRenderer:
    """Clase especializada en dibujar la interfaz de usuario"""
    
    def __init__(self, ventana_width, ventana_height):
        self.ventana_width = ventana_width
        self.ventana_height = ventana_height
    
    def dibujar_barra_energia(self, screen, energia_actual, energia_maxima):
        """Dibuja la barra de energía con estilo avanzado"""
        ancho_barra = 260
        alto_barra = 26
        x_barra = 18
        y_barra = 18
        ratio = max(0, min(1, energia_actual / energia_maxima))
        # Panel translúcido
        panel = pygame.Surface((ancho_barra + 20, alto_barra + 20), pygame.SRCALPHA)
        panel.fill((15, 15, 25, 130))
        screen.blit(panel, (x_barra - 10, y_barra - 10))
        # Fondo barra
        pygame.draw.rect(screen, (70, 25, 25), (x_barra, y_barra, ancho_barra, alto_barra), border_radius=8)
        # Gradiente energía
        gradiente = pygame.Surface((ancho_barra, alto_barra), pygame.SRCALPHA)
        import math
        for x in range(ancho_barra):
            if x/ ancho_barra <= ratio:
                t = x / max(1, ancho_barra)
                r = int(255 - 155 * t)
                g = int(80 + 170 * (1 - abs(t-0.5)*2))
                b = int(40 + 40 * math.sin(t * 3.14))
                pygame.draw.line(gradiente, (r, g, b, 230), (x, 0), (x, alto_barra))
        screen.blit(gradiente, (x_barra, y_barra))
        # Borde
        pygame.draw.rect(screen, (230, 230, 240), (x_barra, y_barra, ancho_barra, alto_barra), 2, border_radius=8)
        # Texto
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(f"Energía {int(energia_actual)}/{int(energia_maxima)}", True, (255,255,255))
        texto_rect = texto.get_rect(center=(x_barra + ancho_barra//2, y_barra + alto_barra//2))
        screen.blit(texto, texto_rect)
    
    def dibujar_estadisticas(self, screen, puntuacion, obstaculos_evitados, energia):
        """Dibuja estadísticas con panel sutil"""
        fuente = pygame.font.Font(None, 28)
        panel = pygame.Surface((210, 90), pygame.SRCALPHA)
        panel.fill((20, 25, 40, 140))
        screen.blit(panel, (20, 60))
        textos = [
            (f"Score: {puntuacion}", (255,255,255)),
            (f"Evitados: {obstaculos_evitados}", (200,220,255)),
            (f"Energía: {int(energia)}", (255,220,180))
        ]
        y = 70
        for txt, col in textos:
            surf = fuente.render(txt, True, col)
            screen.blit(surf, (30, y))
            y += 28
    
    def dibujar_instrucciones(self, screen):
        """Panel lateral de instrucciones con iconos ASCII"""
        fuente_peq = pygame.font.Font(None, 22)
        panel_w = 280
        panel_h = 160
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((15, 20, 35, 150))
        screen.blit(panel, (self.ventana_width - panel_w - 16, 16))
        instrucciones = [
            "↑/↓ o W/S: Carril",
            "ENTER: Salto", 
            "SPACE: Obstáculo (siempre)",
            "T: AVL (siempre)",
            "B: Balance AVL (siempre)",
            "P: Pausa/Despausar",
            "R: Reiniciar"
        ]
        for i, instr in enumerate(instrucciones):
            if "siempre" in instr:
                col = (180, 255, 180)  # Verde claro para controles que funcionan siempre
            else:
                col = (210, 210, 230)  # Color normal
            surf = fuente_peq.render(instr, True, col)
            screen.blit(surf, (self.ventana_width - panel_w + 8, 28 + i*22))
    
    def dibujar_pantalla_pausa(self, screen):
        """Dibuja la pantalla de pausa con controles disponibles"""
        overlay = pygame.Surface((self.ventana_width, self.ventana_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        fuente_grande = pygame.font.Font(None, 72)
        texto_pausa = fuente_grande.render("PAUSADO", True, (255, 255, 255))
        pausa_rect = texto_pausa.get_rect(center=(self.ventana_width//2, self.ventana_height//2 - 80))
        screen.blit(texto_pausa, pausa_rect)
        
        fuente_mediana = pygame.font.Font(None, 32)
        texto_continuar = fuente_mediana.render("Presiona P para continuar", True, (255, 255, 255))
        continuar_rect = texto_continuar.get_rect(center=(self.ventana_width//2, self.ventana_height//2 - 20))
        screen.blit(texto_continuar, continuar_rect)
        
        # Mostrar controles disponibles durante la pausa
        fuente_pequeña = pygame.font.Font(None, 24)
        controles_disponibles = [
            "Controles disponibles durante la pausa:",
            "",
            "SPACE: Agregar obstáculo",
            "T: Mostrar/ocultar árbol AVL",
            "B: Verificar balance del árbol", 
            "R: Reiniciar juego"
        ]
        
        y_start = self.ventana_height//2 + 30
        for i, texto in enumerate(controles_disponibles):
            if i == 0:  # Título
                color = (255, 255, 120)
                fuente_titulo = pygame.font.Font(None, 26)
                surf = fuente_titulo.render(texto, True, color)
            elif texto == "":  # Línea vacía
                continue
            else:  # Controles
                color = (200, 200, 255)
                surf = fuente_pequeña.render(texto, True, color)
            
            texto_rect = surf.get_rect(center=(self.ventana_width//2, y_start + i*25))
            screen.blit(surf, texto_rect)
    
    def dibujar_pantalla_game_over(self, screen, puntuacion_final):
        """Dibuja la pantalla de game over"""
        overlay = pygame.Surface((self.ventana_width, self.ventana_height))
        overlay.set_alpha(180)
        overlay.fill((100, 0, 0))
        screen.blit(overlay, (0, 0))
        
        fuente_grande = pygame.font.Font(None, 72)
        texto_game_over = fuente_grande.render("GAME OVER", True, (255, 255, 255))
        game_over_rect = texto_game_over.get_rect(center=(self.ventana_width//2, self.ventana_height//2 - 80))
        screen.blit(texto_game_over, game_over_rect)
        
        fuente_mediana = pygame.font.Font(None, 48)
        texto_puntuacion = fuente_mediana.render(f"Puntuación Final: {puntuacion_final}", True, (255, 255, 255))
        puntuacion_rect = texto_puntuacion.get_rect(center=(self.ventana_width//2, self.ventana_height//2 - 20))
        screen.blit(texto_puntuacion, puntuacion_rect)
        
        fuente_pequeña = pygame.font.Font(None, 36)
        texto_reiniciar = fuente_pequeña.render("Presiona R para reiniciar", True, (255, 255, 255))
        reiniciar_rect = texto_reiniciar.get_rect(center=(self.ventana_width//2, self.ventana_height//2 + 40))
        screen.blit(texto_reiniciar, reiniciar_rect)

    def dibujar_visualizacion_arbol(self, avl_root):
        from data_structures.avl_visualizer import AVLVisualizer
        visualizador = AVLVisualizer()
        visualizador.visualize(avl_root)
