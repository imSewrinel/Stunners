from common.game_state import GameState
class PlayerState:
    def __init__(self, player_id, hero, game_state:None|GameState = None):
        self.player_id = player_id
        self.hero = hero

        self.game_state = game_state

        self.hp = 30
        self.gold = 3          # طبق داک: شروع بازی 3 طلا
        self.tavern_tier = 1

        self.shop = []
        self.shop_frozen = False

        self.board = []
        self.hand = []

        self.hero_power_uses_left = 0

        # برای Sylvanas (بعداً توسط combat پر می‌شود)
        self.dead_last_combat_card_ids = set()

    def __repr__(self):
        return (
            f"<Player {self.player_id} | Hero={self.hero.name} "
            f"| HP={self.hp} Gold={self.gold} PowerUsesLeft={self.hero_power_uses_left}>"
        )
    
    def ensure_game_state(self):
        if self.game_state is None:
            gs = GameState()
            gs.player_hp = self.hp
            gs.board = self.board  # share list reference
            self.game_state = gs
        else:
            self.game_state.board = self.board
            self.game_state.player_hp = self.hp


      
