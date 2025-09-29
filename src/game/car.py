import os
import pygame

class Car:
    def __init__(self, position, energy, sprite_path=None):
        self.position = position
        self.energy = energy
        self.color = (255, 0, 0)  # fallback
        # Salto
        self.esta_saltando = False
        self.tiempo_salto = 0.0
        self.duracion_salto = 0.9
        self.altura_max_salto = 140  # altura ampliada para asegurar pasar sobre obstáculo de 50px + margen
        self._y_base = None
        # Sprite
        self.sprite = None
        self.sprite_rect = pygame.Rect(0,0,50,50)
        if sprite_path and os.path.exists(sprite_path):
            try:
                img = pygame.image.load(sprite_path).convert_alpha()
                self.sprite = pygame.transform.smoothscale(img, (60,60))
                self.sprite_rect = self.sprite.get_rect()
            except Exception as e:
                print("No se pudo cargar sprite del carro:", e)

    def move(self, distance):
        self.position += distance
        self.energy -= distance * 0.1  # Energy consumption based on distance

    def iniciar_salto(self, y_actual):
        if not self.esta_saltando:
            if self._y_base is None:
                self._y_base = y_actual
            self.esta_saltando = True
            self.tiempo_salto = 0.0

    def actualizar_salto(self, dt, y_actual):
        if not self.esta_saltando:
            return 0
        if self._y_base is None:
            self._y_base = y_actual
        self.tiempo_salto += dt
        prog = self.tiempo_salto / self.duracion_salto
        if prog >= 1.0:
            self.esta_saltando = False
            self.tiempo_salto = 0.0
            return 0
        elev_norm = 4 * prog * (1 - prog)
        elev = elev_norm * self.altura_max_salto
        return -elev

    def update_color(self, new_color):
        self.color = new_color

    def get_position(self):
        return self.position

    def get_energy(self):
        return self.energy

    def is_alive(self):
        return self.energy > 0

    def render(self, window, x_screen, y_screen):
        if self.sprite:
            r = self.sprite.get_rect()
            r.topleft = (x_screen, y_screen)
            window.screen.blit(self.sprite, r)
        else:
            rect = pygame.Rect(x_screen, y_screen, 50, 50)
            pygame.draw.rect(window.screen, self.color, rect)