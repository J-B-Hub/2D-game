class Obstacle:
    def update(self):
        # Example: move obstacle to the left (for demonstration)
        self.x -= 3
    def __init__(self, x, y, obstacle_type):
        self.x = x
        self.y = y
        self.obstacle_type = obstacle_type
        self.width = 50
        self.height = 50

    def check_collision(self, car):
        # Simple collision detection logic
        if (self.x < car.x < self.x + self.width) and (self.y < car.y < self.y + self.height):
            return True
        return False

    def render(self, screen, custom_rect=None, blink=False):
        import pygame
        # Render the obstacle on the screen
        if blink:
            # Blink effect: skip drawing every other frame
            return
        if self.obstacle_type == "rock":
            color = (139, 69, 19)  # Brown color for rock
        elif self.obstacle_type == "tree":
            color = (34, 139, 34)  # Green color for tree
        else:
            color = (255, 0, 0)  # Red color for unknown type

        rect = custom_rect if custom_rect is not None else pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, color, rect)