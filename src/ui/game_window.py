from pygame import display, event, QUIT, Color, Rect, draw

class GameWindow:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.screen = display.set_mode((self.width, self.height))
        display.set_caption(self.title)
        self.clock = None

    def clear(self):
        self.screen.fill(Color('white'))

    def draw_button(self, rect, text):
        from pygame import font
        draw.rect(self.screen, Color('green'), rect)
        font.init()
        font_obj = font.SysFont(None, 48)
        text_surface = font_obj.render(text, True, Color('white'))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def update(self):
        display.flip()

    def handle_events(self):
        for e in event.get():
            if e.type == QUIT:
                return True
        return False

    def draw_obstacle(self, obstacle_rect):
        draw.rect(self.screen, Color('red'), obstacle_rect)

    def draw_car(self, car_rect):
        draw.rect(self.screen, Color('blue'), car_rect)

    def set_clock(self, fps):
        self.clock = display.time.Clock()
        self.clock.tick(fps)