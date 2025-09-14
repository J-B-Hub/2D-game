from matplotlib import pyplot as plt

class AVLVisualizer:
    """
    Clase mejorada para dibujar un árbol AVL usando matplotlib.
    """

    def visualize(self, root):
        """
        Dibuja el árbol AVL a partir de la raíz.
        Cada nodo se dibuja como un círculo con su valor y detalles.
        """
        plt.figure(figsize=(10, 7))
        ax = plt.gca()
        ax.axis('off')
        ax.set_facecolor('#f0f8ff')  # Fondo suave

        def dibujar_nodo(node, x, y, dx):
            if node is None:
                return
            # Dibuja el nodo con borde más grueso y color diferente
            circle = plt.Circle((x, y), 0.6, color='#90caf9', ec='#1565c0', lw=2, zorder=2)
            ax.add_artist(circle)
            # Muestra información extra si existe
            texto = str(node.value)
            if hasattr(node, 'tipo'):
                texto += f"\n{node.tipo}"
            if hasattr(node, 'x') and hasattr(node, 'y'):
                texto += f"\n({node.x},{node.y})"
            ax.text(x, y, texto, fontsize=13, ha='center', va='center', color='#0d47a1', zorder=3)
            # Dibuja la rama izquierda
            if node.left:
                ax.plot([x, x - dx], [y - 0.6, y - 2 + 0.6], color='#8d6e63', lw=2, zorder=1)
                dibujar_nodo(node.left, x - dx, y - 2, dx / 1.5)
            # Dibuja la rama derecha
            if node.right:
                ax.plot([x, x + dx], [y - 0.6, y - 2 + 0.6], color='#8d6e63', lw=2, zorder=1)
                dibujar_nodo(node.right, x + dx, y - 2, dx / 1.5)

        dibujar_nodo(root, 0, 0, 4)
        plt.title("Árbol AVL de Obstáculos", fontsize=16, color='#1565c0')
        plt.tight_layout()
        plt.show()