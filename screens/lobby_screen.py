from screens.screen_base import Screen
from core.screen_manager import ScreenType
from common.hero import Hero
import pygame


class Lobby_screen(Screen):
    def load(self):
        self.msg = "Choose hero: 1=YOGG  2=LICH_KING  3=SYLVANAS"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                hero = Hero("YOGG", "Yogg-Saron", "Tentacle Gift", 0, "active", uses_per_turn=1)
            elif event.key == pygame.K_2:
                hero = Hero("LICH_KING", "Lich King", "Reborn Blessing", 0, "active", requires_target=True)
            elif event.key == pygame.K_3:
                hero = Hero("SYLVANAS", "Sylvanas", "Death Buff", 0, "active")
            else:
                return

            # assign hero and register player
            self.manager.hero = hero
            player_id = self.manager.player_id
            self.manager.match_state.add_player(player_id, hero)
            self.manager.match_state.start_turn(player_id)
            self.manager.change_screen(ScreenType.GAME)

    def update(self):
        pass

    def render(self):
        self.draw_text("LOBBY", 50, 50, size=40)
        self.draw_text(self.msg, 50, 120)




                
