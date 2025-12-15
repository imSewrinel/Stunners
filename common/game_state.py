class GameState:
    def __init__(self):
        self.board = []
        self.max_board = 7

        self.global_card_buffs = {
            "BEETLE_TOKEN": {"attack": 0, "health": 0},
        }

        self.death_queue = []

    #Board

    def add_to_board(self, minion, position=None):
        if len(self.board) >= self.max_board:
            print("Board is full, cannot summon:", minion.name)
            return False

        self.board.append(minion)
        print("Summoned on board:", minion)
        return True

    def apply_global_buffs(self, minion):
        if minion.card_id in self.global_card_buffs:
            buff = self.global_card_buffs[minion.card_id]
            minion.buff(buff["attack"], buff["health"])

    def summon_minion(self, card_id):
        from common.minion import (
            BeetleToken,
            SkeletonToken,
            BuzzingVermin,
            ForestRover,
            NestSwarmer,
            TurquoiseSkitterer,
            MonstrousMacaw,
            HarmlessBonehead,
        )

        mapping = {
            "BEETLE_TOKEN": BeetleToken,
            "SKELETON_TOKEN": SkeletonToken,
            "BUZZING_VERMIN": BuzzingVermin,
            "FOREST_ROVER": ForestRover,
            "NEST_SWARMER": NestSwarmer,
            "TURQUOISE_SKITTERER": TurquoiseSkitterer,
            "MONSTROUS_MACAW": MonstrousMacaw,
            "HARMLESS_BONEHEAD": HarmlessBonehead,
        }

        if card_id not in mapping:
            print("Unknown card_id:", card_id)
            return False

        minion = mapping[card_id]()
        self.apply_global_buffs(minion)
        return self.add_to_board(minion)

    #Deathrattle trigger (Macaw)

    def trigger_leftmost_friendly_deathrattle(self, exclude_minion=None):
        for m in self.board:
            if exclude_minion and m is exclude_minion:
                continue
            if "Deathrattle" in m.keywords and m.is_alive():
                m.on_deathrattle(self)
                return True
        return False

    #Death processing

    def process_deaths(self):
        for m in self.board[:]:
            if m.dead:
                self.board.remove(m)
                if "Deathrattle" in m.keywords:
                    m.on_deathrattle(self)

    def deal_damage_to_slot(self, idx, dmg):
        if idx >= len(self.board):
            return
        self.board[idx].take_damage(dmg)
        self.process_deaths()

    def debug_print_board(self):
        print("=== BOARD STATE ===")
        for i, m in enumerate(self.board):
            print(f"{i}: {m}")
        print("===================")
