from core.screen_base import Screen

class ResultScreen(Screen):
    def load(self):
        self.state = self.manager.game_state
        self.match = self.manager.match_state
        self.player = self.match.get_player(self.manager.player_id)

    def update(self):
        print("Game Over!")
        print("Board HP (game_state.player_hp):", self.state.player_hp)
        print("Player HP (player_state.hp):", self.player.hp)
        raise SystemExit()

    def render(self):
        pass    

