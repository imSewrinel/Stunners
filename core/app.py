import pygame
from utils import load_assets
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

        self.screen = pygame.display.set_mode((width, height))
        # Load assets (images)
        self.assets = load_assets()
        if not self.assets:
            print(f"Warning: no assets found in {BASE_IMAGE_PATH!r}")
        pygame.display.set_caption(caption)

        # Setup a simple game state and populate a few minions for demo
        self.game_state = GameState()
        if not self.game_state.board:
            self.game_state.play_minion(BuzzingVermin())
            self.game_state.play_minion(ForestRover())
            self.game_state.play_minion(NestSwarmer())

        # mapping from card_id to asset key (docs-based fallbacks)
        self.minion_asset_map = {
            "BUZZING_VERMIN": "minions/BG31_803_render_80",
            "FOREST_ROVER": "minions/BG31_801_render_80",
            "NEST_SWARMER": "minions/BG31_807_render_80",
        }

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
        # Draw board minions as simple sprites near the bottom of the screen
        # Layout: centered horizontally, spaced evenly
        board = getattr(self, 'game_state', None) and self.game_state.board or []
        n = len(board)
        if n == 0:
            return

        slot_width = 120
        slot_height = 120
        total_width = slot_width * n
        start_x = max(20, (self.width - total_width) // 2)
        y = self.height - slot_height - 40

        for i, m in enumerate(board):
            # find an asset for this minion
            surf = self._asset_for_minion(m) if hasattr(self, '_asset_for_minion') else None
            if surf is None:
                # skip if nothing to draw
                continue
            # scale to slot size while preserving aspect ratio
            w, h = surf.get_size()
            scale = min(slot_width / w, slot_height / h)
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            img = pygame.transform.smoothscale(surf, new_size)

            x = start_x + i * slot_width + (slot_width - new_size[0]) // 2
            self.screen.blit(img, (x, y))

            # draw stat text (attack/health)
            try:
                font = pygame.font.SysFont(None, 20)
                stat_text = f"{m.attack}/{m.health}"
                txt_surf = font.render(stat_text, True, (255, 255, 255))
                txt_rect = txt_surf.get_rect()
                txt_rect.center = (x + new_size[0] // 2, y + new_size[1] + 12)
                self.screen.blit(txt_surf, txt_rect)
            except Exception:
                pass

    def _asset_for_minion(self, minion):
        # try explicit mapping first
        key = self.minion_asset_map.get(minion.card_id)
        if key and key in self.assets:
            return self.assets[key]

        # try fuzzy match by name
        name_token = minion.name.lower().replace(' ', '_')
        for k in self.assets.keys():
            if k.startswith('minions/') and name_token in k.lower():
                return self.assets[k]

        # fallback: first minion asset
        for k, v in self.assets.items():
            if k.startswith('minions/'):
                return v
        return None

    def run(self) -> None:
        self.running = True
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0

            self.handle_events()
            self.update()

            self.screen.fill((0, 0, 0))
            self.draw()

            pygame.display.flip()

        try:
            pygame.quit()
        except Exception:
            pass

    def stop(self) -> None:
        self.running = False
