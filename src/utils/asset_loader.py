import os
import pygame

_cache = {}

# Mapeo de tipos a nombres de archivo por defecto
DEFAULT_MAP = {
    'car': 'car.png',
    'rock': 'rock.png',
    'tree': 'tree.png',
    'pothole': 'pothole.png'
}

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'assets')
ASSETS_DIR = os.path.abspath(ASSETS_DIR)


def load_image(name, size=None, colorkey=None):
    """Carga una imagen desde assets con cache y escalado opcional."""
    if name in _cache and size in (None, _cache[name][1]):
        surf, stored_size = _cache[name]
        if size is None or stored_size == size:
            return surf
    path = os.path.join(ASSETS_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Imagen no encontrada: {path}")
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.smoothscale(img, size)
    _cache[name] = (img, size)
    return img


def load_for_type(tipo, fallback_color=(255,0,0), size=(50,50)):
    filename = DEFAULT_MAP.get(tipo, None)
    if not filename:
        return None
    try:
        return load_image(filename, size=size)
    except Exception:
        # Si falla, devolvemos una superficie coloreada
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(fallback_color)
        return surf
