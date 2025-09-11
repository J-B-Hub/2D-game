class Car:
    def __init__(self, position, energy):
        self.position = position
        self.energy = energy
        self.color = (255, 0, 0)  # Default color red

    def move(self, distance):
        self.position += distance
        self.energy -= distance * 0.1  # Energy consumption based on distance

    def jump(self):
        # Logic for jumping (e.g., avoiding obstacles)
        pass

    def update_color(self, new_color):
        self.color = new_color

    def get_position(self):
        return self.position

    def get_energy(self):
        return self.energy

    def is_alive(self):
        return self.energy > 0

    def render(self, window):
        # Draw the car as a rectangle using its position and color
        import pygame
        car_rect = pygame.Rect(self.position, 500, 50, 100)  # Example y, width, height
        window.draw_car(car_rect)