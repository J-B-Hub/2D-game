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
        def calcular_dimensiones(node, depth=0):
            if node is None:
                return 0, depth
            left_width, left_depth = calcular_dimensiones(getattr(node, 'left', None), depth + 1)
            right_width, right_depth = calcular_dimensiones(getattr(node, 'right', None), depth + 1)
            return max(left_width, right_width) + 1, max(left_depth, right_depth)
        
        width, height = calcular_dimensiones(root)
        fig_width = max(12, width * 2)
        fig_height = max(8, height * 1.5)
        
        plt.figure(figsize=(fig_width, fig_height))
        ax = plt.gca()
        ax.axis('off')
        ax.set_facecolor('#f0f8ff')
        ax.set_xlim(-width * 2.5, width * 2.5)
        ax.set_ylim(-height * 2.5, 1)

        def dibujar_nodo(node, x, y, dx):
            if node is None:
                return
            circle = plt.Circle((x, y), 0.5, color='#90caf9', ec='#1565c0', lw=2, zorder=2)
            ax.add_artist(circle)
            if hasattr(node, 'obstacle') and node.obstacle is not None:
                texto = f"({node.obstacle.x:.0f}, {node.obstacle.y:.0f})\n{getattr(node.obstacle, 'obstacle_type', '')}"
            else:
                texto = "Sin obstáculo"
            ax.text(x, y, texto, fontsize=9, ha='center', va='center', color='#0d47a1', zorder=3, weight='bold')
            if hasattr(node, 'left') and node.left:
                ax.plot([x, x - dx], [y - 0.5, y - 2.2 + 0.5], color='#8d6e63', lw=2, zorder=1)
                dibujar_nodo(node.left, x - dx, y - 2.2, dx / 1.4)
            if hasattr(node, 'right') and node.right:
                ax.plot([x, x + dx], [y - 0.5, y - 2.2 + 0.5], color='#8d6e63', lw=2, zorder=1)
                dibujar_nodo(node.right, x + dx, y - 2.2, dx / 1.4)

        dibujar_nodo(root, 0, 0, width * 0.8)
        plt.title("Árbol AVL de Obstáculos", fontsize=16, color='#1565c0', pad=20)

        if root:
            def pre(n, acc):
                if not n: return
                acc.append(n.x_position)
                pre(n.left, acc); pre(n.right, acc)
            def ino(n, acc):
                if not n: return
                ino(n.left, acc); acc.append(n.x_position); ino(n.right, acc)
            def post(n, acc):
                if not n: return
                post(n.left, acc); post(n.right, acc); acc.append(n.x_position)
            pre_l, in_l, post_l = [], [], []
            pre(root, pre_l); ino(root, in_l); post(root, post_l)
            txt = "Pre:  " + ", ".join(map(str, pre_l))[:140]
            txt += "\nIn:   " + ", ".join(map(str, in_l))[:140]
            txt += "\nPost: " + ", ".join(map(str, post_l))[:140]
            ax.text(width * 1.2, -0.5, txt,
                    ha='left', va='top', fontsize=9,
                    bbox=dict(facecolor='white', alpha=0.75, edgecolor='#1565c0', boxstyle='round,pad=0.4'),
                    color='#0d47a1')

        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        mngr = plt.get_current_fig_manager()
        try:
            mngr.toolbar.pan()
        except Exception:
            pass
        plt.show()