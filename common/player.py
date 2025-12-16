class PlayerState:
    def __init__(self, player_id, hero):
        self.player_id = player_id
        self.hero = hero

        self.hp = 30
        self.gold = 0
        self.tavern_tier = 1

        self.board = []
        self.hand = []

        # هر نوبت ریست می‌شود (طبق uses_per_turn هیرو)
        self.hero_power_uses_left = 0

        # برای Sylvanas (بعداً تو Combat پر می‌شود)
        self.dead_last_combat_card_ids = set()

    def __repr__(self):
        return (
            f"<Player {self.player_id} | Hero={self.hero.name} "
            f"| HP={self.hp} Gold={self.gold} PowerUsesLeft={self.hero_power_uses_left}>"
        )

      
