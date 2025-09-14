from matplotlib import pyplot as plt

class AVLVisualizer:
    """
    Clase sencilla para dibujar un árbol AVL usando matplotlib.
    """

    def visualize(self, root):
        """
        Dibuja el árbol AVL a partir de la raíz.
        Cada nodo se dibuja como un círculo con su valor.
        """
        plt.figure(figsize=(8, 6))
        ax = plt.gca()
        ax.axis('off')  # Oculta los ejes

        # Función interna para recorrer y dibujar el árbol
        def dibujar_nodo(node, x, y, dx):
            if node is None:
                return
            # Dibuja el nodo como un círculo
            circle = plt.Circle((x, y), 0.5, color='lightblue', ec='black')
            ax.add_artist(circle)
            # Escribe el valor del nodo en el círculo
            ax.text(x, y, str(node.value), fontsize=12, ha='center', va='center')
            # Dibuja la rama izquierda
            if node.left:
                ax.plot([x, x - dx], [y - 0.5, y - 2 + 0.5], color='black')
                dibujar_nodo(node.left, x - dx, y - 2, dx / 1.5)
            # Dibuja la rama derecha
            if node.right:
                ax.plot([x, x + dx], [y - 0.5, y - 2 + 0.5], color='black')
                dibujar_nodo(node.right, x + dx, y - 2, dx / 1.5)

        # Comienza a dibujar desde la raíz
        dibujar_nodo(root, 0, 0, 4)
        plt.title("Árbol AVL de Obstáculos")
        plt.show()