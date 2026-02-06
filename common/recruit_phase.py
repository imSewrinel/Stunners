from __future__ import annotations
from typing import List, Optional, Dict, Any
from common.match_state import MatchState
from common.game_state import GameState
from common.player import PlayerState
from common.minion import ( # Aded Minions untill now
    BeetleToken, SkeletonToken, HandToken,
    BuzzingVermin, ForestRover, NestSwarmer, TurquoiseSkitterer, MonstrousMacaw,
    HarmlessBonehead, HandlessForsaken, NerubianDeathswarmer,
    WrathWeaver,
)
from config import *


# --------- Minion factory (card_id -> class) ---------
_MINION_FACTORY = {
    "BEETLE_TOKEN": BeetleToken,
    "SKELETON_TOKEN": SkeletonToken,
    "HAND_TOKEN": HandToken,

    "BUZZING_VERMIN": BuzzingVermin,
    "FOREST_ROVER": ForestRover,
    "NEST_SWARMER": NestSwarmer,
    "TURQUOISE_SKITTERER": TurquoiseSkitterer,
    "MONSTROUS_MACAW": MonstrousMacaw,

    "HARMLESS_BONEHEAD": HarmlessBonehead,
    "HANDLESS_FORSAKEN": HandlessForsaken,
    "NERUBIAN_DEATHSWARMER": NerubianDeathswarmer,

    "WRATH_WEAVER": WrathWeaver,
}


def create_minion(card_id: str):
    cls = _MINION_FACTORY.get(card_id)
    if cls is None:
        raise ValueError(f"Unknown card_id: {card_id}")
    return cls()



# ------------- Recruit class -------------
class RecruitError(Exception):
    pass

class RecruitPhase:
    """Recruit phase engine: shop, buy, play, sell, refresh, freeze, upgrade.

    It is intentionally UI-agnostic.
    - Shop is stored on PlayerState as `shop: List[str]` (card_ids)
    - Freeze flag stored as `shop_frozen: bool`
    - Hand stores Minion instances
    - Board stores Minion instances
    """

    def __init__(self, match: MatchState):
        self.match = match

    # ----- Shop helpers -----
    def _get_or_init_shop_fields(self, player: PlayerState) -> None:
        if not hasattr(player, "shop"):
            player.shop = []
        if not hasattr(player, "shop_frozen"):
            player.shop_frozen = False

    def _allowed_pool(self, tier: int) -> List[str]:
        # according to typical BG rules: shop shows minions with minion.tier <= tavern_tier
        allowed: List[str] = []
        for t in range(1, tier + 1):
            allowed.extend(self.match.minion_pool_by_tier.get(t, []))
        return allowed

    def roll_shop(self, player_id:str) -> List[str]:
        player = self.match.get_player(player_id)
        self._get_or_init_shop_fields(player)

        allowed = self._allowed_pool(player.tavern_tier)
        if not allowed:
            player.shop = []
            return player.shop

        player.shop = [self.match.rng.choice(allowed) for 
                       _ in range(TAVERN_SIZE_BASE_ON_TIRE[player.tavern_tier])]
        return player.shop

    def start_recruit(self, player_id:str, round_no:int = 1) -> Dict[str, Any]:
        """Start recruit for one player: gain gold (handled by MatchState.start_turn) + roll shop."""
        player = self.match.get_player(player_id)
        self._get_or_init_shop_fields(player)

        # MatchState.start_turn already increments gold by 1 up to 10.
        self.match.start_turn(player_id, round_no)

        if not player.shop_frozen:
            self.roll_shop(player_id)

        return {
            "player_id": player_id,
            "gold": player.gold,
            "tavern_tier": player.tavern_tier,
            "shop": list(player.shop),
            "shop_frozen": player.shop_frozen,
        }

    # ----- Actions -----
    def refresh(self, player_id:str) -> Dict[str, Any]:
        player = self.match.get_player(player_id)
        self._get_or_init_shop_fields(player)

        if player.shop_frozen:
            raise RecruitError("Shop is frozen. Unfreeze first.")
        
        if player.hero.hero_id != "MILLHOUSE_MANASTORM":
            if not self.match.spend_gold(player_id, REFRESH_STORE_COINS):
                raise RecruitError("Not enough gold to refresh.")
        else:
            if not self.match.spend_gold(player_id, REFRESH_STORE_COINS_FOR_Millhouse_Manastorm):
                raise RecruitError("Not enough gold to refresh.")
        
        self.roll_shop(player_id)
        return {"type": "REFRESH", "gold": player.gold, "shop": list(player.shop)}

    def freeze(self, player_id:str, value: bool = True) -> Dict[str, Any]:
        player = self.match.get_player(player_id)
        self._get_or_init_shop_fields(player)
        player.shop_frozen = bool(value)
        return {"type": "FREEZE", "shop_frozen": player.shop_frozen}

    def buy(self, player_id:str, shop_index: int) -> Dict[str, Any]:
        player = self.match.get_player(player_id)
        self._get_or_init_shop_fields(player)

        if shop_index < 0 or shop_index >= len(player.shop):
            raise RecruitError("Invalid shop index.")
        
        if len(player.hand) >= MAX_MINIOS_IN_HAND:
            raise RecruitError("Hand is full.")
    
        if player.hero.hero_id != "MILLHOUSE_MANASTORM":
            if not self.match.spend_gold(player_id, BUY_MINION_COINS):
                raise RecruitError("Not enough gold to buy.")
        else:
            if not self.match.spend_gold(player_id, BUY_MINION_COINS_FOR_Millhouse_Manastorm):
                raise RecruitError("Not enough gold to buy.")
        
        card_id = player.shop.pop(shop_index)
        minion = create_minion(card_id)
        player.hand.append(minion)

        return {"type": "BUY", "card_id": card_id, "gold": player.gold, "hand_size": len(player.hand)}

    def play(self, player_id:str, hand_index: int, board_pos: Optional[int] = None) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if hand_index < 0 or hand_index >= len(player.hand):
            raise RecruitError("Invalid hand index.")
        
        if len(player.board) >= MAX_MINIOS_IN_BOARD:
            raise RecruitError("Board is full.")

        minion = player.hand.pop(hand_index)

        player.ensure_game_state()
        # GameState.play_minion handles battlecry + global buffs + wrath weaver triggers
        ok = player.game_state.play_minion(minion, position=board_pos)

        if not ok:
            # revert
            player.hand.insert(hand_index, minion)
            raise RecruitError("Failed to play minion.")
        
        return {"type": "PLAY", "card_id": minion.card_id, "hp": player.hp, "board_size": len(player.board)}

    def sell(self, player_id:str, board_index: int, refund: int = 1) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if board_index < 0 or board_index >= len(player.board):
            raise RecruitError("Invalid board index.")
        
        sold = player.board.pop(board_index)
        player.gold = min(10, player.gold + refund)
        
        return {"type": "SELL", "card_id": sold.card_id, "gold": player.gold}

    def upgrade_tavern(self, player_id:str) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if player.tavern_tier == 4:
            raise RecruitError("Tavern already max tier.")
        
        base_cost_by_tier = {1: 5,
                             2: 7, 
                             3: 8, 
                             4: 9}
        cost = base_cost_by_tier.get(player.tavern_tier)
        if player.hero.hero_id == "MILLHOUSE_MANASTORM": # hero power
            cost += 1

        if not self.match.spend_gold(player_id, cost):
            raise RecruitError("Not enough gold to upgrade tavern.")
        
        player.tavern_tier += 1
        # shop stays; next refresh/turn uses higher tier
        return {"type": "UPGRADE", "new_tier": player.tavern_tier, "gold": player.gold, "cost": cost}

