class TreeNode:
    """Nodo simple del árbol AVL"""
    def __init__(self, x_position):
        self.x_position = x_position  # Posición X como clave del nodo
        self.obstacle = None          # El obstáculo que está en esta posición
        self.height = 1              # Altura del nodo para balanceo
        self.left = None             # Hijo izquierdo
        self.right = None            # Hijo derecho

class AVLTree:
    """Árbol AVL simplificado para manejar obstáculos del juego"""
    
    def __init__(self):
        self.root = None
    
    def buscar_obstaculos_visibles(self, x_min, x_max):
        """Busca obstáculos que están en el rango de visión del jugador"""
        obstaculos_encontrados = []
        self._buscar_en_rango(self.root, x_min, x_max, obstaculos_encontrados)
        return obstaculos_encontrados
    
    def _buscar_en_rango(self, nodo, x_min, x_max, lista_obstaculos):
        """Método privado para buscar obstáculos en un rango"""
        if nodo is None:
            return
        
        # Si el nodo está en el rango, agregarlo
        if x_min <= nodo.x_position <= x_max and nodo.obstacle is not None:
            lista_obstaculos.append(nodo.obstacle)
        
        # Buscar en hijo izquierdo si es necesario
        if nodo.x_position > x_min and nodo.left is not None:
            self._buscar_en_rango(nodo.left, x_min, x_max, lista_obstaculos)
        
        # Buscar en hijo derecho si es necesario
        if nodo.x_position < x_max and nodo.right is not None:
            self._buscar_en_rango(nodo.right, x_min, x_max, lista_obstaculos)
    
    def insertar_obstaculo(self, obstaculo):
        """Inserta un obstáculo en el árbol usando su posición X como clave"""
        self.root = self._insertar_nodo(self.root, obstaculo.x)
        
        # Buscar el nodo recién insertado y asignar el obstáculo
        nodo_encontrado = self._buscar_nodo(self.root, obstaculo.x)
        if nodo_encontrado:
            nodo_encontrado.obstacle = obstaculo
    
    def _insertar_nodo(self, nodo, x_position):
        """Método privado para insertar un nodo en el árbol"""
        # 1. Inserción normal como en un BST
        if nodo is None:
            return TreeNode(x_position)
        
        if x_position < nodo.x_position:
            nodo.left = self._insertar_nodo(nodo.left, x_position)
        elif x_position > nodo.x_position:
            nodo.right = self._insertar_nodo(nodo.right, x_position)
        else:
            return nodo  # Ya existe un nodo con esta posición
        
        # 2. Actualizar altura del nodo
        nodo.height = 1 + max(self._obtener_altura(nodo.left), 
                              self._obtener_altura(nodo.right))
        
        # 3. Balancear el árbol
        return self._balancear_nodo(nodo, x_position)
    
    def _buscar_nodo(self, nodo, x_position):
        """Busca un nodo específico por su posición X"""
        if nodo is None or nodo.x_position == x_position:
            return nodo
        
        if x_position < nodo.x_position:
            return self._buscar_nodo(nodo.left, x_position)
        else:
            return self._buscar_nodo(nodo.right, x_position)
    
    def eliminar_obstaculo(self, x_position):
        """Elimina un obstáculo del árbol por su posición X"""
        self.root = self._eliminar_nodo(self.root, x_position)
    
    def _eliminar_nodo(self, nodo, x_position):
        """Método privado para eliminar un nodo"""
        if nodo is None:
            return nodo
        
        if x_position < nodo.x_position:
            nodo.left = self._eliminar_nodo(nodo.left, x_position)
        elif x_position > nodo.x_position:
            nodo.right = self._eliminar_nodo(nodo.right, x_position)
        else:
            # Este es el nodo a eliminar
            if nodo.left is None:
                return nodo.right
            elif nodo.right is None:
                return nodo.left
            
            # Nodo con dos hijos: encontrar el sucesor
            sucesor = self._encontrar_minimo(nodo.right)
            nodo.x_position = sucesor.x_position
            nodo.obstacle = sucesor.obstacle
            nodo.right = self._eliminar_nodo(nodo.right, sucesor.x_position)
        
        # Actualizar altura y balancear
        nodo.height = 1 + max(self._obtener_altura(nodo.left), 
                              self._obtener_altura(nodo.right))
        return self._balancear_nodo(nodo, x_position)
    
    def _encontrar_minimo(self, nodo):
        """Encuentra el nodo con el valor mínimo"""
        while nodo.left is not None:
            nodo = nodo.left
        return nodo

    
    def _balancear_nodo(self, nodo, x_position):
        """Balancea el árbol después de una inserción o eliminación"""
        if nodo is None:
            return nodo
            
        balance = self._obtener_balance(nodo)
        
        # Rotación a la derecha (caso izquierda-izquierda)
        if balance > 1:
            if nodo.left and self._obtener_balance(nodo.left) >= 0:
                return self._rotar_derecha(nodo)
            # Caso izquierda-derecha
            elif nodo.left and self._obtener_balance(nodo.left) < 0:
                nodo.left = self._rotar_izquierda(nodo.left)
                return self._rotar_derecha(nodo)
        
        # Rotación a la izquierda (caso derecha-derecha)
        if balance < -1:
            if nodo.right and self._obtener_balance(nodo.right) <= 0:
                return self._rotar_izquierda(nodo)
            # Caso derecha-izquierda
            elif nodo.right and self._obtener_balance(nodo.right) > 0:
                nodo.right = self._rotar_derecha(nodo.right)
                return self._rotar_izquierda(nodo)
        
        return nodo
    
    def _rotar_izquierda(self, nodo_z):
        """Rotación simple a la izquierda"""
        if nodo_z is None or nodo_z.right is None:
            return nodo_z
            
        nodo_y = nodo_z.right
        temp = nodo_y.left
        
        # Realizar rotación
        nodo_y.left = nodo_z
        nodo_z.right = temp
        
        # Actualizar alturas
        nodo_z.height = 1 + max(self._obtener_altura(nodo_z.left), 
                                self._obtener_altura(nodo_z.right))
        nodo_y.height = 1 + max(self._obtener_altura(nodo_y.left), 
                                self._obtener_altura(nodo_y.right))
        
        return nodo_y
    
    def _rotar_derecha(self, nodo_z):
        """Rotación simple a la derecha"""
        if nodo_z is None or nodo_z.left is None:
            return nodo_z
            
        nodo_y = nodo_z.left
        temp = nodo_y.right
        
        # Realizar rotación
        nodo_y.right = nodo_z
        nodo_z.left = temp
        
        # Actualizar alturas
        nodo_z.height = 1 + max(self._obtener_altura(nodo_z.left), 
                                self._obtener_altura(nodo_z.right))
        nodo_y.height = 1 + max(self._obtener_altura(nodo_y.left), 
                                self._obtener_altura(nodo_y.right))
        
        return nodo_y
    
    def _obtener_altura(self, nodo):
        """Obtiene la altura de un nodo"""
        if nodo is None:
            return 0
        return nodo.height
    
    def _obtener_balance(self, nodo):
        """Calcula el factor de balance de un nodo"""
        if nodo is None:
            return 0
        return self._obtener_altura(nodo.left) - self._obtener_altura(nodo.right)
    
    def obtener_lista_ordenada(self):
        """Devuelve una lista de obstáculos ordenados por posición X"""
        obstaculos = []
        self._recorrer_inorden(self.root, obstaculos)
        return obstaculos
    
    def _recorrer_inorden(self, nodo, lista):
        """Recorrido inorden para obtener obstáculos ordenados"""
        if nodo is not None:
            self._recorrer_inorden(nodo.left, lista)
            if nodo.obstacle is not None:
                lista.append(nodo.obstacle)
            self._recorrer_inorden(nodo.right, lista)
    
    def limpiar_arbol(self):
        """Elimina todos los obstáculos del árbol"""
        self.root = None