import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt

class AVLVisualizer:
    """
    Clase mejorada para dibujar un árbol AVL usando matplotlib.
    """

    def visualize(self, root):
        """
        Dibuja el árbol AVL a partir de la raíz.
        Cada nodo se dibuja como un círculo con los datos del obstáculo.
        """
        # Calcular dimensiones del árbol para ajustar la figura
        def calcular_dimensiones(node, depth=0):
            if node is None:
                return 0, depth
            left_width, left_depth = calcular_dimensiones(getattr(node, 'left', None), depth + 1)
            right_width, right_depth = calcular_dimensiones(getattr(node, 'right', None), depth + 1)
            return max(left_width, right_width) + 1, max(left_depth, right_depth)
        
        width, height = calcular_dimensiones(root)
        
        # Ajustar el tamaño de la figura según las dimensiones del árbol
        fig_width = max(12, width * 2)
        fig_height = max(8, height * 1.5)
        
        plt.figure(figsize=(fig_width, fig_height))
        ax = plt.gca()
        ax.axis('off')
        ax.set_facecolor('#f0f8ff')  # Fondo suave
        
        # Ajustar los límites del plot para evitar que se corten los círculos
        ax.set_xlim(-width * 2.5, width * 2.5)
        ax.set_ylim(-height * 2.5, 1)

        def dibujar_nodo(node, x, y, dx):
            if node is None:
                return
            # Dibuja el nodo con borde más grueso y color diferente
            circle = plt.Circle((x, y), 0.5, color='#90caf9', ec='#1565c0', lw=2, zorder=2)
            ax.add_artist(circle)
            # Muestra información del obstáculo si existe
            if hasattr(node, 'obstacle') and node.obstacle is not None:
                texto = f"({node.obstacle.x:.0f}, {node.obstacle.y:.0f})\n{getattr(node.obstacle, 'obstacle_type', '')}"
            else:
                texto = "Sin obstáculo"
            ax.text(x, y, texto, fontsize=9, ha='center', va='center', color='#0d47a1', zorder=3, weight='bold')
            # Dibuja la rama izquierda
            if hasattr(node, 'left') and node.left:
                ax.plot([x, x - dx], [y - 0.5, y - 2.2 + 0.5], color='#8d6e63', lw=2, zorder=1)
                dibujar_nodo(node.left, x - dx, y - 2.2, dx / 1.4)
            # Dibuja la rama derecha
            if hasattr(node, 'right') and node.right:
                ax.plot([x, x + dx], [y - 0.5, y - 2.2 + 0.5], color='#8d6e63', lw=2, zorder=1)
                dibujar_nodo(node.right, x + dx, y - 2.2, dx / 1.4)

        dibujar_nodo(root, 0, 0, width * 0.8)
        plt.title("Árbol AVL de Obstáculos", fontsize=16, color='#1565c0', pad=20)
        
        # Habilitar herramientas de navegación (zoom y pan)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        mngr = plt.get_current_fig_manager()
        mngr.toolbar.pan()  # Activar herramienta de navegación por defecto
        
        plt.show()