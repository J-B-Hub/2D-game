import pygame

class InputManager:
    """Clase especializada en manejar las entradas del jugador"""
    
    def __init__(self):
        self.teclas_presionadas = {}
        self.contador_frames = 0
    
    def actualizar_entradas(self, contador_frames):
        """Actualiza el estado de las teclas presionadas"""
        self.contador_frames = contador_frames
        self.teclas_presionadas = pygame.key.get_pressed()
    
    def quiere_pausar(self):
        """Verifica si el jugador quiere pausar/despausar"""
        return self.teclas_presionadas[pygame.K_p] and self.contador_frames % 10 == 0
    
    def quiere_reiniciar(self):
        """Verifica si el jugador quiere reiniciar"""
        return self.teclas_presionadas[pygame.K_r] and self.contador_frames % 10 == 0
    
    def quiere_mostrar_arbol(self):
        """Verifica si el jugador quiere mostrar/ocultar el árbol"""
        return self.teclas_presionadas[pygame.K_t] and self.contador_frames % 10 == 0
    
    def quiere_agregar_obstaculo(self):
        """Verifica si el jugador quiere agregar un obstáculo"""
        return self.teclas_presionadas[pygame.K_SPACE] and self.contador_frames % 30 == 0

    def quiere_saltar(self):
        """Salto con tecla Enter (RETURN)"""
        return self.teclas_presionadas[pygame.K_RETURN] and self.contador_frames % 5 == 0

    def quiere_verificar_balance(self):
        """Tecla B para verificar balance AVL"""
        return self.teclas_presionadas[pygame.K_b] and self.contador_frames % 15 == 0

    def quiere_debug(self):
        """Tecla D para debug overlay AVL"""
        return self.teclas_presionadas[pygame.K_d] and self.contador_frames % 15 == 0
    
    def quiere_mover_arriba(self):
        """Verifica si el jugador quiere mover el carro arriba"""
        return self.teclas_presionadas[pygame.K_UP] or self.teclas_presionadas[pygame.K_w]
    
    def quiere_mover_abajo(self):
        """Verifica si el jugador quiere mover el carro abajo"""
        return self.teclas_presionadas[pygame.K_DOWN] or self.teclas_presionadas[pygame.K_s]
