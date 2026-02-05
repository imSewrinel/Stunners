from config import *

class Screen:
    def __init__(self, manger):
        self.manager = manger

    def get_font(self, size=28): # One special font in different sizes
        if size not in FONT_CACHE:
            FONT_CACHE[size] = pygame.font.SysFont("Arial", size)
        return FONT_CACHE[size]

    def draw_text(self, text, x, y, size=28, color=(255, 255, 255)):
        surf = self.get_font(size).render(text, True, color)
        self._last_screen = pygame.display.get_surface()
        self._last_screen.blit(surf, (x, y))

    def load(self):
        pass
    
    def unload(self):
        pass

    def handle_event(self, event):
        pass

    def update(self):
        pass    

    def render(self):
        pass



