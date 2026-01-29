import pygame
from utils import get_meta, Lazy_assets
from config import *
from common.game_state import GameState
from common.minion import BuzzingVermin, ForestRover, NestSwarmer

class GameManager:
    def __init__(self, width: int, height: int, caption: str, fps: int) -> None:
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            # If mixer errors to init (continue without sound)
            pass

        self.width = width
        self.height = height
        self.caption = caption
        self.fps = fps

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)

        # Load assets 
        self.assets_meta = get_meta()
        self.Lazy_assets_handler = Lazy_assets(self.assets_meta)

        self.clock = pygame.time.Clock()
        self.running = False
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
                return

    def update(self) -> None:
        pass

    def draw(self) -> None:
        # lazy assets test
        battlefield_img = self.Lazy_assets_handler.build("battlefield/battlefield_Pandaria")
        battlefield_img = pygame.transform.scale(battlefield_img, (self.width, self.height))
        self.screen.blit(battlefield_img)

    def run(self) -> None:
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update()

            self.draw()

            pygame.display.flip()

        try:
            pygame.quit()
        except Exception:
            pass

    def stop(self) -> None:
        self.running = False