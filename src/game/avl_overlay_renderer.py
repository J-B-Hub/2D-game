import pygame

class AVLMiniRenderer:
    """
    Renderiza una vista mini del árbol AVL dentro del juego (overlay en tiempo real).
    Estético y ligero: sin matplotlib, sólo Pygame.
    """
    def __init__(self, screen_width, screen_height, width=250, height=170, margin=12):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = width
        self.height = height
        self.margin = margin
        self.font_small = pygame.font.Font(None, 18)
        self.font_tiny = pygame.font.Font(None, 14)
        self.bg_cache = None
        self._cache_size = (width, height)

    # -------- Utilidades internas --------
    def _calc_heights(self, node):
        if not node:
            return 0
        hl = self._calc_heights(node.left)
        hr = self._calc_heights(node.right)
        node._tmp_height_overlay = max(hl, hr) + 1
        return node._tmp_height_overlay

    def _balance(self, node):
        if not node:
            return 0
        hl = getattr(node.left, '_tmp_height_overlay', 0) if node.left else 0
        hr = getattr(node.right, '_tmp_height_overlay', 0) if node.right else 0
        return hl - hr

    def _collect_nodes(self, root):
        """Devuelve lista de (node, depth, order_index) usando inorden para orden horizontal."""
        nodes = []
        index = 0
        def inorder(n, depth):
            nonlocal index
            if not n: return
            inorder(n.left, depth + 1)
            nodes.append((n, depth, index))
            index += 1
            inorder(n.right, depth + 1)
        inorder(root, 0)
        return nodes

    def _draw_panel_background(self):
        """Genera (o reutiliza) fondo degradado semi-transparente con borde."""
        if self.bg_cache is not None:
            return self.bg_cache
        surf = pygame.Surface(self._cache_size, pygame.SRCALPHA)
        for y in range(self.height):
            t = y / max(1, self.height - 1)
            # Gradiente azul oscuro -> gris azulado
            r = int(20 + 40 * t)
            g = int(30 + 60 * t)
            b = int(50 + 80 * t)
            a = int(180)  # semi-transparente
            pygame.draw.line(surf, (r, g, b, a), (0, y), (self.width, y))
        # Borde
        pygame.draw.rect(surf, (180, 200, 230, 200), surf.get_rect(), 2, border_radius=10)
        self.bg_cache = surf
        return surf

    def dibujar(self, screen, root):
        panel_x = self.screen_width - self.width - self.margin
        panel_y = self.screen_height - self.height - self.margin
        panel_rect = pygame.Rect(panel_x, panel_y, self.width, self.height)

        # Fondo
        bg = self._draw_panel_background()
        screen.blit(bg, (panel_x, panel_y))

        if not root:
            texto = self.font_small.render("AVL vacío", True, (230, 235, 240))
            screen.blit(texto, texto.get_rect(center=(panel_x + self.width//2, panel_y + self.height//2)))
            return

        # Preparar datos
        self._calc_heights(root)
        nodes = self._collect_nodes(root)
        if not nodes:
            return
        max_index = max(idx for (_, _, idx) in nodes)
        max_depth = max(d for (_, d, _) in nodes)
        usable_w = self.width - 30
        usable_h = self.height - 42
        base_x = panel_x + 12
        base_y = panel_y + 26  # dejar espacio para título (ligeramente más compacto)

        # Mapa para buscar posición de nodos (x,y)
        positions = {}
        # Calcular coordenadas
        for node, depth, order_index in nodes:
            if max_index == 0:
                x = base_x + usable_w // 2
            else:
                x = base_x + int(order_index / max_index * usable_w)
            y = base_y + int((depth / max(1, max_depth)) * usable_h)
            positions[node] = (x, y)

        # Dibujar conexiones primero
        for node, depth, order_index in nodes:
            x, y = positions[node]
            if node.left and node.left in positions:
                xl, yl = positions[node.left]
                pygame.draw.line(screen, (90, 110, 140), (x, y), (xl, yl), 2)
            if node.right and node.right in positions:
                xr, yr = positions[node.right]
                pygame.draw.line(screen, (90, 110, 140), (x, y), (xr, yr), 2)

        # Dibujar nodos
        for node, depth, order_index in nodes:
            x, y = positions[node]
            bal = self._balance(node)
            # Color según balance
            if abs(bal) > 1:
                color = (239, 83, 80)      # rojo - desbalance
            elif abs(bal) == 1:
                color = (255, 202, 40)     # amarillo
            elif bal == 0:
                color = (102, 187, 106)    # verde
            else:
                color = (66, 165, 245)     # azul fallback
            radius = 10
            pygame.draw.circle(screen, color, (x, y), radius)
            pygame.draw.circle(screen, (15, 25, 35), (x, y), radius, 2)
            # Texto interno (x_position reducido)
            label = str(int(getattr(node, 'x_position', 0)))
            if len(label) > 3:
                label = label[-3:]
            txt = self.font_tiny.render(label, True, (10, 10, 15))
            screen.blit(txt, txt.get_rect(center=(x, y)))

        # Título y metadatos
        titulo = self.font_small.render("AVL Obstáculos", True, (210, 220, 235))
        screen.blit(titulo, (panel_x + 12, panel_y + 5))
        meta = self.font_tiny.render(f"Nodos: {len(nodes)} Prof: {max_depth+1}", True, (180, 195, 210))
        screen.blit(meta, (panel_x + self.width - meta.get_width() - 10, panel_y + 6))

        # Leyenda rápida (opcional minimalista)
        legend_y = panel_y + self.height - 14
        legend_items = [
            ((102,187,106), 'OK'),
            ((255,202,40), '±1'),
            ((239,83,80), '>1')
        ]
        lx = panel_x + 12
        for col, tag in legend_items:
            pygame.draw.circle(screen, col, (lx, legend_y), 5)
            lab = self.font_tiny.render(tag, True, (220, 225, 235))
            screen.blit(lab, (lx + 10, legend_y - lab.get_height()//2))
            lx += 10 + lab.get_width() + 12
