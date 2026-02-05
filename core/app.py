import pygame
from utils import get_meta, Lazy_assets
from config import *
from common.game_state import GameState
from common.minion import BuzzingVermin, ForestRover, NestSwarmer
from core.screen_manager import ScreenManager, ScreenType
from screens.login_screen import LoginScreen
from screens.lobby_screen import LobbyScreen
from screens.game_screen import GameScreen
from screens.result_screen import ResultScreen
from config import *


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

        # Screen manager that controls app screens
        self.screen_manager = ScreenManager()
        self.screen_manager.app = self  # give screens access to app if needed

        # Register lightweight pygame-based screens here so many files aren't required
        self.screen_manager.register(ScreenType.LOGIN, LoginScreen)
        self.screen_manager.register(ScreenType.LOBBY, LobbyScreen)
        self.screen_manager.register(ScreenType.GAME, GameScreen)
        self.screen_manager.register(ScreenType.RESULT, ResultScreen)

        # Start on login (start the game)
        self.screen_manager.change_screen(ScreenType.LOGIN)

    def handle_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.stop()
                return
            if self.screen_manager.current_screen:
                try:
                    self.screen_manager.current_screen.handle_event(event)
                except Exception:
                    pass

    def update(self) -> None:
        # Let current screen update game logic
        self.screen_manager.update()

    def draw(self) -> None:
        # lazy assets test
        battlefield_img = self.Lazy_assets_handler.build("battlefield/battlefield_Pandaria")
        battlefield_img = pygame.transform.scale(battlefield_img, (self.width, self.height))
        self.screen.blit(battlefield_img)
        # Let current screen render to surface
        if self.screen_manager.current_screen:
            try:
                self.screen_manager.current_screen.render()
            except Exception:
                pass

    def run(self) -> None:
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update()

            self.draw()

            pygame.display.flip()

    def stop(self) -> None:
        self.running = False