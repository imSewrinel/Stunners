from screens.screen_base import Screen
import pygame


class ResultScreen(Screen):
    def load(self):
        try:
            self.player = self.manager.match_state.get_player(self.manager.player_id)
        except KeyError:
            # No player registered
            self.player = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # stop the app
                if hasattr(self.manager, "app"):
                    self.manager.app.stop()

    def render(self):
        self.draw_text("RESULT", 50, 50, size=40)
        if self.player:
            self.draw_text(f"Player HP: {self.player.hp}", 50, 120)
        else:
            self.draw_text("No player registered", 50, 120)


#     def load(self):
#         self.state = self.manager.game_state
#         self.match = self.manager.match_state
#         try:
#             self.player = self.match.get_player(self.manager.player_id)
#         except Exception:
#             # No player registered
#             self.player = None

#     def update(self):
#         print("Game Over!")
#         print("Board HP (game_state.player_hp):", self.state.player_hp)
#         print("Player HP (player_state.hp):", self.player.hp)
#         raise SystemExit()

#     def render(self):
#         pass    

