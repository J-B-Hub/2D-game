import pygame

class CollisionDetector:
    """Clase especializada en detectar colisiones entre el carro y obstáculos"""
    
    def __init__(self):
        pass
    
    def verificar_colisiones(self, carro_x, carro_y, obstaculos_visibles, posicion_en_carretera, estado_juego,
                              desplazamiento_vertical=0, esta_saltando=False):
        """Verifica colisiones. Si está saltando y elevación suficiente, se ignora obstáculo."""
        y_final = carro_y + desplazamiento_vertical
        recticulo_altura = 50
        rectangulo_carro = pygame.Rect(carro_x, y_final, 50, recticulo_altura)
        
        for obstaculo in obstaculos_visibles:
            # Calcular posición del obstáculo en pantalla
            x_pantalla = obstaculo.x - posicion_en_carretera + carro_x
            rectangulo_obstaculo = pygame.Rect(x_pantalla, obstaculo.y, obstaculo.width, obstaculo.height)
            
            # Verificar colisión
            colision_detectada = False
            
            # Para obstáculos tipo 'hole', solo se pueden evitar saltando suficientemente alto
            if obstaculo.obstacle_type == 'hole':
                # Los holes requieren salto obligatorio - no se pueden evitar por carriles
                if esta_saltando and (y_final + recticulo_altura) < (obstaculo.y + obstaculo.height * 0.3):
                    pass  # Salto exitoso sobre el hole
                else:
                    # Si no está saltando lo suficiente, verificar colisión con hole
                    if rectangulo_carro.colliderect(rectangulo_obstaculo):
                        colision_detectada = True
            else:
                # Lógica normal para otros obstáculos
                if esta_saltando and (y_final + recticulo_altura) < (obstaculo.y + obstaculo.height * 0.4):
                    pass  # Salto exitoso sobre obstáculo normal
                else:
                    if rectangulo_carro.colliderect(rectangulo_obstaculo):
                        colision_detectada = True
            
            # Procesar resultado de la colisión
            if colision_detectada:
                estado_juego.agregar_obstaculo_golpeado(obstaculo, esta_saltando)
            else:
                # Si pasó el obstáculo sin chocar, contar como evitado
                if (obstaculo.x < posicion_en_carretera and 
                    obstaculo not in estado_juego.obstaculos_golpeados):
                    estado_juego.contar_obstaculo_evitado()
    
    def hay_colision(self, rect1, rect2):
        """Verifica si dos rectángulos colisionan"""
        return rect1.colliderect(rect2)
    
    def crear_rectangulo_carro(self, x, y, ancho=50, alto=50):
        """Crea el rectángulo de colisión del carro"""
        return pygame.Rect(x, y, ancho, alto)
    
    def crear_rectangulo_obstaculo(self, obstaculo, x_pantalla):
        """Crea el rectángulo de colisión de un obstáculo"""
        return pygame.Rect(x_pantalla, obstaculo.y, obstaculo.width, obstaculo.height)
