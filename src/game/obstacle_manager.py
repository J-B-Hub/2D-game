from data_structures.avl_tree import AVLTree
from game.obstacle import Obstacle
import random

class ObstacleManager:
    """Clase simple para manejar obstáculos usando un árbol AVL"""
    
    def __init__(self):
        self.arbol = AVLTree()
        self.obstaculos_iniciales = []
    
    def cargar_obstaculos_iniciales(self, lista_obstaculos):
        """Carga los obstáculos desde la configuración JSON"""
        self.obstaculos_iniciales = lista_obstaculos.copy()
        for datos_obstaculo in lista_obstaculos:
            obstaculo = Obstacle(
                x=datos_obstaculo['x'],
                y=datos_obstaculo['y'], 
                obstacle_type=datos_obstaculo['type']
            )
            self.arbol.insertar_obstaculo(obstaculo)
    
    def obtener_obstaculos_visibles(self, posicion_carro):
        """Obtiene los obstáculos que el jugador puede ver"""
        x_minimo = posicion_carro - 200  # 200 píxeles atrás
        x_maximo = posicion_carro + 1000  # 1000 píxeles adelante
        return self.arbol.buscar_obstaculos_visibles(x_minimo, x_maximo)
    
    def agregar_obstaculo_nuevo(self, x, y, tipo):
        """Agrega un nuevo obstáculo al árbol"""
        nuevo_obstaculo = Obstacle(x=x, y=y, obstacle_type=tipo)
        self.arbol.insertar_obstaculo(nuevo_obstaculo)
        print(f"Obstáculo agregado en posición ({x}, {y}) de tipo {tipo}")
    
    def eliminar_obstaculos_pasados(self, posicion_carro):
        """Elimina obstáculos que ya pasó el jugador para ahorrar memoria"""
        limite_eliminar = posicion_carro - 300
        obstaculos_todos = self.arbol.obtener_lista_ordenada()
        
        for obstaculo in obstaculos_todos:
            if obstaculo.x < limite_eliminar:
                self.arbol.eliminar_obstaculo(obstaculo.x)
                print(f"Obstáculo eliminado en posición {obstaculo.x}")
    
    def reiniciar_obstaculos(self):
        """Vuelve a cargar los obstáculos iniciales"""
        self.arbol.limpiar_arbol()
        self.cargar_obstaculos_iniciales(self.obstaculos_iniciales)
        print("Obstáculos reiniciados")
    
    def crear_obstaculo_aleatorio(self, posicion_carro):
        """Crea un obstáculo aleatorio adelante del carro"""
        tipos_obstaculos = ["rock", "tree", "pothole", "hole"]
        carriles_y = [225, 325]  # Posiciones Y de los carriles
        
        x_nuevo = posicion_carro + random.randint(400, 800)
        tipo_nuevo = random.choice(tipos_obstaculos)
        
        # Los holes tienen posición Y fija (empezando en carril superior)
        if tipo_nuevo == 'hole':
            y_nuevo = 225  # Posición Y fija para holes (carril superior, se extiende hacia abajo)
        else:
            y_nuevo = random.choice(carriles_y)
        
        self.agregar_obstaculo_nuevo(x_nuevo, y_nuevo, tipo_nuevo)
