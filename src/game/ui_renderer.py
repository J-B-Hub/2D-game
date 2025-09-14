import pygame
from data_structures.avl_visualizer import AVLVisualizer
class UIRenderer:
    """Clase especializada en dibujar la interfaz de usuario"""
    
    def __init__(self, ventana_width, ventana_height):
        self.ventana_width = ventana_width
        self.ventana_height = ventana_height
    
    def dibujar_barra_energia(self, screen, energia_actual, energia_maxima):
        """Dibuja la barra de energía del jugador"""
        ancho_barra = 200
        alto_barra = 20
        x_barra = 10
        y_barra = 10
        
        # Fondo de la barra (rojo)
        pygame.draw.rect(screen, (255, 0, 0), (x_barra, y_barra, ancho_barra, alto_barra))
        
        # Energía actual (verde)
        ancho_energia = int(ancho_barra * (energia_actual / energia_maxima))
        pygame.draw.rect(screen, (0, 255, 0), (x_barra, y_barra, ancho_energia, alto_barra))
        
        # Borde de la barra
        pygame.draw.rect(screen, (255, 255, 255), (x_barra, y_barra, ancho_barra, alto_barra), 2)
    
    def dibujar_estadisticas(self, screen, puntuacion, obstaculos_evitados, energia):
        """Dibuja las estadísticas del juego"""
        fuente = pygame.font.Font(None, 36)
        
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
        texto_evitados = fuente.render(f"Evitados: {obstaculos_evitados}", True, (255, 255, 255))
        texto_energia = fuente.render(f"Energía: {int(energia)}", True, (255, 255, 255))
        
        screen.blit(texto_puntuacion, (10, 40))
        screen.blit(texto_evitados, (10, 70))
        screen.blit(texto_energia, (220, 10))
    
    def dibujar_instrucciones(self, screen):
        """Dibuja las instrucciones de control"""
        fuente_pequeña = pygame.font.Font(None, 24)
        instrucciones = [
            "Flechas/WASD: Mover carro",
            "SPACE: Agregar obstáculo", 
            "T: Mostrar/ocultar árbol",
            "P: Pausar",
            "R: Reiniciar"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            texto = fuente_pequeña.render(instruccion, True, (200, 200, 200))
            screen.blit(texto, (self.ventana_width - 250, 10 + i * 25))
    
    def dibujar_pantalla_pausa(self, screen):
        """Dibuja la pantalla de pausa"""
        overlay = pygame.Surface((self.ventana_width, self.ventana_height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        fuente_grande = pygame.font.Font(None, 72)
        texto_pausa = fuente_grande.render("PAUSADO", True, (255, 255, 255))
        pausa_rect = texto_pausa.get_rect(center=(self.ventana_width//2, self.ventana_height//2 - 50))
        screen.blit(texto_pausa, pausa_rect)
        
        fuente_pequeña = pygame.font.Font(None, 36)
        texto_continuar = fuente_pequeña.render("Presiona P para continuar", True, (255, 255, 255))
        continuar_rect = texto_continuar.get_rect(center=(self.ventana_width//2, self.ventana_height//2 + 20))
        screen.blit(texto_continuar, continuar_rect)
    
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
    

    
    
    # def dibujar_visualizacion_arbol(self, screen, obstaculos_ordenados):
    #     """Dibuja una visualización simple del árbol AVL"""
    #     # Overlay semi-transparente
    #     overlay = pygame.Surface((self.ventana_width, self.ventana_height))
    #     overlay.set_alpha(200)
    #     overlay.fill((50, 50, 50))
    #     screen.blit(overlay, (0, 0))
        
    #     # Título
    #     fuente_titulo = pygame.font.Font(None, 48)
    #     titulo = fuente_titulo.render("Visualización del Árbol AVL", True, (255, 255, 255))
    #     titulo_rect = titulo.get_rect(center=(self.ventana_width//2, 30))
    #     screen.blit(titulo, titulo_rect)
        
    #     # Dibujar lista simple de obstáculos
    #     fuente = pygame.font.Font(None, 24)
    #     y_actual = 80
        
    #     for i, obstaculo in enumerate(obstaculos_ordenados[:15]):  # Máximo 15 para que quepa en pantalla
    #         texto = f"{i+1}. Posición X: {int(obstaculo.x)}, Y: {int(obstaculo.y)}, Tipo: {obstaculo.obstacle_type}"
    #         superficie_texto = fuente.render(texto, True, (255, 255, 255))
    #         screen.blit(superficie_texto, (50, y_actual))
    #         y_actual += 30
        
    #     # Instrucciones
    #     instruccion = fuente.render("Presiona T para ocultar", True, (255, 255, 0))
    #     screen.blit(instruccion, (50, self.ventana_height - 50))

