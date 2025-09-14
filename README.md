# Juego 2D

## Descripción General
Este proyecto es un juego 2D desarrollado en Python, con una arquitectura modular que facilita la extensión y el mantenimiento. El juego incluye gestión de objetos, detección de colisiones, renderizado gráfico y manejo de entradas del usuario.

---

## Estructura del Proyecto

```
config/
    game_config.json         # Configuración general del juego
src/
    main.py                  # Punto de entrada principal
    data_structures/
        avl_tree.py          # Árbol AVL para estructuras de datos eficientes
    game/
        car.py               # Lógica y atributos del coche/jugador
        collision_detector.py# Detección de colisiones
        game_engine.py       # Motor principal del juego
        game_renderer.py     # Renderizado de elementos gráficos
        game_state.py        # Estado actual del juego
        input_manager.py     # Manejo de entradas del usuario
        obstacle_manager.py  # Gestión de obstáculos
        obstacle.py          # Lógica de obstáculos
        road_renderer.py     # Renderizado de la carretera
        ui_renderer.py       # Renderizado de la interfaz de usuario
    ui/
        game_window.py       # Ventana principal del juego
    utils/
        constants.py         # Constantes globales
        json_loader.py       # Utilidad para cargar JSON
```

---

## Componentes y Clases Principales

### main.py
- Punto de entrada. Inicializa la ventana, carga configuración y arranca el motor del juego.

### data_structures/avl_tree.py
- `AVLTree`: Estructura de datos eficiente para búsquedas y actualizaciones.

### game/car.py
- `Car`: Representa el coche/jugador, con métodos para moverse y detectar colisiones.

### game/collision_detector.py
- `CollisionDetector`: Métodos para detectar colisiones entre objetos.

### game/game_engine.py
- `GameEngine`: Controla la lógica principal, el bucle de actualización y la interacción entre componentes.

### game/game_renderer.py
- `GameRenderer`: Dibuja los elementos del juego en pantalla.

### game/game_state.py
- `GameState`: Gestiona el estado actual del juego (puntuación, nivel, vidas).

### game/input_manager.py
- `InputManager`: Captura y procesa las entradas del usuario.

### game/obstacle_manager.py & game/obstacle.py
- `ObstacleManager`, `Obstacle`: Generan y gestionan obstáculos.

### game/road_renderer.py
- `RoadRenderer`: Dibuja la carretera y gestiona su desplazamiento.

### game/ui_renderer.py
- `UIRenderer`: Dibuja la interfaz de usuario (UI).

### ui/game_window.py
- `GameWindow`: Crea y gestiona la ventana principal del juego.

### utils/constants.py
- Define valores constantes usados en todo el proyecto.

### utils/json_loader.py
- Funciones para cargar archivos JSON.

### config/game_config.json
- Parámetros ajustables del juego (velocidad, dificultad, controles).

---

## Flujo General del Juego

1. **Inicialización:**
   - Se carga la configuración desde `game_config.json`.
   - Se crea la ventana principal (`GameWindow`).
   - Se inicializan los componentes del juego.

2. **Bucle Principal:**
   - Se capturan las entradas del usuario.
   - Se actualizan los estados de los objetos.
   - Se detectan colisiones.
   - Se renderizan los elementos gráficos.

3. **Gestión de Estados:**
   - Se actualiza la puntuación, vidas y otros datos relevantes.
   - Se gestiona el avance de niveles y el fin del juego.

---

##