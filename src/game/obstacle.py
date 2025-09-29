import pygame
from utils.asset_loader import load_for_type

class Obstacle:
    def __init__(self, x, y, obstacle_type):
        self.x = x
        self.y = y
        self.obstacle_type = obstacle_type
        # Tamaños diferenciados
        if obstacle_type == 'tree':
            self.width, self.height = 60, 80
        elif obstacle_type == 'rock':
            self.width, self.height = 60, 60
        elif obstacle_type == 'pothole':
            self.width, self.height = 70, 40
        else:
            self.width, self.height = 55, 55
        self.sprite = load_for_type(obstacle_type, size=(self.width, self.height))

    def update(self):
        # Si hubiese lógica de movimiento independiente, aquí se aplicaría
        pass

    def check_collision(self, car):
        base_y = getattr(car, '_y_base', None)
        if base_y is None:
            return False
        return (self.x < car.position < self.x + self.width) and (self.y < base_y < self.y + self.height)

    def render(self, screen, custom_rect=None, blink=False):
        if blink:
            return
        rect = custom_rect if custom_rect is not None else pygame.Rect(self.x, self.y, self.width, self.height)
        if self.sprite:
            screen.blit(self.sprite, rect)
        else:
            pygame.draw.rect(screen, (255,0,0), rect)