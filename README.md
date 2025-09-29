<div align="center">

# 🚗 Juego 2D con Árbol AVL en Vivo

_Un pequeño proyecto educativo en Python que mezcla un minijuego de esquivar obstáculos con una visualización viva de una estructura de datos (Árbol AVL)._  
Diseñado para ser claro, modular y fácil de extender.

</div>

---

## 🧠 ¿Qué es este proyecto?
Es un juego 2D: controlas un carro que avanza por una carretera horizontal y esquiva obstáculos (rocas, árboles, huecos).  
Mientras juegas, en la esquina inferior derecha aparece un panel que muestra en tiempo real un **árbol AVL** que almacena los obstáculos por su posición X. Así puedes ver cómo crece y se balancea la estructura mientras el juego sigue.

El objetivo principal del proyecto es **aprender arquitectura modular** y **visualizar estructuras de datos** dentro de un contexto lúdico.

---

## ✨ Características Principales
- Arquitectura modular (cada responsabilidad en su archivo/clase).
- Árbol AVL integrado: inserción, eliminación y visualización mini en vivo.
- Salto parabólico para esquivar obstáculos (con altura suficiente si está bien sincronizado).
- Barra de energía con degradado dinámico.
- Fondo con cielo degradado y carretera estilizada.
- Sprites para carro y obstáculos (con fallback si falta la imagen).
- Overlay AVL compacto con colores según balance del nodo:
  - Verde: balance perfecto (0)
  - Amarillo: ±1 (estable)
  - Rojo: desbalance detectado (>1 en valor absoluto)
- Teclas para depuración rápida (balance, generar obstáculos, etc.).

---

## 🕹️ Controles
| Tecla | Acción |
|-------|--------|
| ENTER | Saltar |
| Flecha arriba / W | Cambiar a carril superior |
| Flecha abajo / S  | Cambiar a carril inferior |
| SPACE | Generar un nuevo obstáculo adelante |
| T | Mostrar / ocultar overlay del AVL |
| B | Verificar balance del árbol (mensaje en consola) |
| D | Debug rápido: imprime número de nodos y estado del overlay |
| P | Pausar / reanudar |
| R | Reiniciar juego completo |
| Cerrar ventana | Salir |

El overlay del árbol **ya aparece activo al inicio**. Si estorba, puedes ocultarlo con T.

---

## 🚀 Cómo Ejecutar
1. (Opcional pero recomendado) Crear entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # o en Windows: venv\Scripts\activate
   ```
2. Instalar dependencias (si añades un requirements.txt más adelante):
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el juego:
   ```bash
   python3 src/main.py
   ```
4. (Para salir del entorno):
   ```bash
   deactivate
   ```

> Nota: Si no tienes sprites, el juego usará formas simples como respaldo.

---

## 🗂️ Estructura del Proyecto (Vista Amigable)
```
config/                # Configuración (JSON)
src/
  main.py              # Entrada principal
  data_structures/
    avl_tree.py        # Implementación del árbol AVL
    avl_visualizer.py  # (Versión matplotlib, ahora opcional)
  game/
    car.py             # Lógica del carro (salto, energía)
    game_engine.py     # Orquesta todo (inputs, lógica, render)
    game_renderer.py   # Dibuja fondo, carretera, UI y overlay
    avl_overlay_renderer.py # Mini renderer en tiempo real del AVL
    obstacle.py        # Clase Obstacle
    obstacle_manager.py# Inserta/gestiona obstáculos con AVL
    collision_detector.py # Verifica colisiones
    road_renderer.py   # Carretera estilizada
    ui_renderer.py     # Paneles, barra energía, textos
    input_manager.py   # Teclas → intención de jugador
    game_state.py      # Puntuación, energía, flags
  ui/
    game_window.py     # Abstrae la ventana pygame
  utils/
    asset_loader.py    # Carga y cache de sprites
    constants.py       # Ancho, alto, FPS, etc.
    json_loader.py     # Carga configuración
assets/                # Imágenes (car.png, rock.png...)
```

---

## 🔁 ¿Qué pasa en cada frame?
1. Se leen las teclas (no se actúa directo, se consultan intenciones).
2. Se aplican acciones (saltar, generar obstáculo, pausar, etc.).
3. El carro “avanza” virtualmente (incrementa posición horizontal lógica).
4. Se piden obstáculos “visibles” al árbol AVL dado un rango (ventana de visión).
5. Se detectan colisiones (ignoradas si el salto eleva suficiente al carro).
6. Se remueven obstáculos que ya quedaron muy atrás.
7. Se dibuja: cielo → carretera → carro → obstáculos → UI → overlay AVL.

---

## 🌳 ¿Por qué un Árbol AVL?
En vez de guardar los obstáculos en una simple lista y recorrerla cada vez:
- El AVL mantiene los nodos balanceados.
- Permite buscar obstáculos dentro de un rango (ventana visible) sin explorar todo.
- Inserciones y eliminaciones se mantienen eficientes aunque crezca el juego.

Visualmente, el mini panel ayuda a “ver” la estructura interna mientras se juega.

Colores de nodos:
- Verde: estable (balance 0)
- Amarillo: ligeramente inclinado (±1)
- Rojo: desbalance (te ayuda a notar si algo falló en las rotaciones)

---

## 🏗️ Arquitectura Modular (Explicado Simple)
- Cada archivo tiene una única responsabilidad clara.
- El motor (`game_engine.py`) NO dibuja ni detecta colisiones directamente: delega.
- El renderer no toma decisiones de juego: sólo pinta.
- El árbol AVL vive dentro de `ObstacleManager` y es consultado según necesidad.
- El overlay se alimenta de la raíz del árbol sin modificar la lógica.

Beneficios:
- Fácil de cambiar una parte sin romper otra.
- Puedes sustituir el AVL por otra estructura (ej: segment tree) sin tocar el motor.
- Permite enseñar separación de responsabilidades.

---

## 🧪 Mecánicas Especiales
### Salto
Curva suave (parábola) calculada con el tiempo transcurrido. Mientras esté en el aire, la colisión se ignora si la elevación supera parte de la altura del obstáculo.

### Energía
Barra que puede servir para ampliar mecánicas (turbo, penalizaciones, etc.). Visualmente se rellena con un degradado.

### Overlay AVL
Se redibuja cada frame. No usa matplotlib (para que no bloquee). Es compacto, semitransparente y no interfiere con la jugabilidad.

---

## 🧩 Cómo Extender
| Quiero... | Cambiar / Agregar |
|-----------|-------------------|
| Añadir tipo de obstáculo | `obstacle.py`, `obstacle_manager.py`, sprite en assets/ |
| Cambiar física del salto | `car.py` (método actualizar_salto) |
| Mejorar carretera | `road_renderer.py` |
| Añadir sonido | Crear módulo `sound_manager.py` y llamarlo desde el motor |
| Reemplazar AVL | Nueva estructura en `data_structures/` y adaptar `ObstacleManager` |
| Guardar puntuaciones | Nueva clase `score_manager.py` + archivo JSON |

---

## 🛠️ Solución de Problemas
| Problema | Posible Causa | Solución |
|----------|---------------|----------|
| No aparece sprite del carro | Falta `assets/car.png` | Colocar imagen o dejar que use rectángulo |
| Overlay no se ve | Se ocultó con T | Presiona T de nuevo |
| Saltos no esquivan | Tiempo de salto mal sincronizado | Salta un poco antes del obstáculo |
| Se cierra al iniciar | Pygame no instalado | `pip install pygame` |
| Árbol siempre vacío | No hay generación | Pulsa SPACE varias veces |

---

## 📦 Entorno Virtual (Resumen Rápido)
```bash
python3 -m venv venv
source venv/bin/activate   # (Windows: venv\Scripts\activate)
pip install -r requirements.txt  # si existe
python3 src/main.py
deactivate
```

---

## 🔮 Ideas Futuras
- Partículas al saltar.
- Sonidos y música.
- Power-ups (escudo, energía extra, ralentizar tiempo).
- Dificultad progresiva (más obstáculos según puntuación).
- Exportar el árbol a JSON en caliente.
- Reemplazar la carretera por un “modo noche” dinámico.

---

## ❓ FAQ Rápido
**¿Necesito entender AVL para jugar?** No, pero verlo en vivo ayuda a aprender.

**¿Hace falta el visualizador de matplotlib?** Ya no; el overlay interno es suficiente (el archivo sigue por referencia educativa).

**¿Puedo poner pantalla completa?** Puedes modificar la creación de la ventana en `game_window.py`.

**¿Cómo cambio la velocidad?** Ajusta valores en `config/game_config.json` o en `constants.py`.

---

## 🙌 Créditos
Proyecto académico / educativo. Puedes reutilizarlo para aprender, enseñar o experimentar.

Si mejoras algo interesante, ¡compártelo! 🚀

---

