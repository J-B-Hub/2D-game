import pygame
from utils.json_loader import load_config
from game.car import Car
from game.obstacle_manager import ObstacleManager
from game.game_engine import GameEngineModular
from ui.game_window import GameWindow
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Función principal del juego - versión modular"""
    # Inicializar Pygame
    pygame.init()
    print("Pygame inicializado") 
    
    # Cargar configuración desde JSON
    configuracion = load_config('config/game_config.json')
    print("Configuración cargada")
    
    # Crear ventana del juego
    titulo_juego = configuracion.get('title', '2D Car Game - Versión Modular')
    ventana = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, titulo_juego)
    print("Ventana del juego creada")
    
    # Mostrar pantalla de inicio
    mostrar_pantalla_inicio(ventana)
    
    # Crear objetos principales del juego
    import os
    ruta_carro = 'assets/car.png'
    if not os.path.exists(ruta_carro):
        print("[Aviso] No se encontró assets/car.png, usando rectángulo por defecto.")
        ruta_carro = None
    carro = Car(position=0, energy=configuracion.get('initial_energy', 100), sprite_path=ruta_carro)
    gestor_obstaculos = ObstacleManager()
    motor_juego = GameEngineModular(carro, gestor_obstaculos, ventana, configuracion)
    
    # Cargar obstáculos iniciales desde la configuración
    obstaculos_iniciales = configuracion.get('obstacles', [])
    gestor_obstaculos.cargar_obstaculos_iniciales(obstaculos_iniciales)
    print(f"Cargados {len(obstaculos_iniciales)} obstáculos iniciales")
    
    # Verificar configuración de la meta
    distancia_meta = configuracion.get('meta_distance', 6000)
    print(f"Meta establecida a {distancia_meta} metros")
    
    # Ejecutar el juego
    print("Iniciando juego modular...")
    motor_juego.ejecutar()
    
    # Limpiar y salir
    pygame.quit()
    print("Juego terminado")

def mostrar_pantalla_inicio(ventana):
    """Muestra una pantalla de inicio simple"""
    esperando_click = True
    
    # Crear botón de inicio
    boton_ancho = 200
    boton_alto = 80
    boton_x = SCREEN_WIDTH // 2 - boton_ancho // 2
    boton_y = SCREEN_HEIGHT // 2 - boton_alto // 2
    rectangulo_boton = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
    
    while esperando_click:
        # Limpiar pantalla
        ventana.clear()
        
        # Dibujar título
        fuente_titulo = pygame.font.Font(None, 64)
        texto_titulo = fuente_titulo.render("2D Car Game", True, (255, 255, 255))
        titulo_rect = texto_titulo.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        ventana.screen.blit(texto_titulo, titulo_rect)
        
        # Dibujar subtítulo
        fuente_subtitulo = pygame.font.Font(None, 32)
        texto_subtitulo = fuente_subtitulo.render("2D Game", True, (200, 200, 200))
        subtitulo_rect = texto_subtitulo.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        ventana.screen.blit(texto_subtitulo, subtitulo_rect)
        
        # Dibujar botón
        ventana.draw_button(rectangulo_boton, "JUGAR")
        
        # Dibujar información sobre la arquitectura
        fuente_info = pygame.font.Font(None, 20)
        info_lineas = [
            "🧩 Arquitectura Modular:",
            "• InputManager: Maneja entradas del teclado",
            "• GameState: Controla estado del juego",
            "• CollisionDetector: Detecta colisiones",
            "• GameRenderer: Coordina renderizado",
            "• RoadRenderer: Dibuja la carretera",
            "• UIRenderer: Dibuja la interfaz",
            "• GameEngine: Solo coordina todo"
        ]
        
        y_info = SCREEN_HEIGHT//2 + 60
        for linea in info_lineas:
            texto = fuente_info.render(linea, True, (150, 150, 150))
            texto_rect = texto.get_rect(center=(SCREEN_WIDTH//2, y_info))
            ventana.screen.blit(texto, texto_rect)
            y_info += 25
        
        # Actualizar pantalla
        ventana.update()
        
        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if rectangulo_boton.collidepoint(evento.pos):
                    esperando_click = False
                    print("¡Comenzando juego modular!")

if __name__ == "__main__":
    main()
