from __future__ import annotations
from typing import List, Optional, Dict, Any
from common.match_state import MatchState
from common.game_state import GameState
from common.player import PlayerState
from common.minion import *
from config import *


# ------------- Recruit class -------------
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
        self.round: int = 0

    def _allowed_pool(self, tier: int) -> List[str]:
        # shop shows minions with minion.tier <= tavern_tier
        allowed: List[str] = []
        for t in range(1, tier + 1):
            allowed.extend(self.match.minion_pool_by_tier.get(t, []))
        return allowed

    def roll_shop(self, player_id:str) -> List[str]:
        player = self.match.get_player(player_id)

        allowed = self._allowed_pool(player.tavern_tier)
        if not allowed:
            player.shop = []
            return player.shop
        
        if not player.shop_frozen:
            player.shop = [self.match.rng.choice(allowed) for 
                        _ in range(TAVERN_SIZE_BASE_ON_TIRE[player.tavern_tier])]
            return player.shop
        else:
            # TODO: it should be completted 
            pass

        return player.shop

    def show_shop(self, player_id:str):
        player = self.match.get_player(player_id)
        print("________ Current minions in Bob's Tavern: ________")
        for index, minion in enumerate(player.shop):
            print(f"{index+1}: {minion}")
        print("\n")

    def show_hand(self, player_id:str):
        player = self.match.get_player(player_id)
        print("________ Current minions in hand: ________")
        for index, minion in enumerate(player.hand):
            print(f"{index+1}: {minion}")
        print("\n")

    def show_board(self, player_id:str):
        player = self.match.get_player(player_id)
        print("________ Current minions on board: ________")
        for index, minion in enumerate(player.board):
            print(f"{index+1}: {minion}")
        print("\n")

    def start_recruit(self, player_id:str) -> Dict[str, Any]:
        self.round += 1
        """Start recruit for one player: gain gold (handled by MatchState.start_turn) + roll shop."""
        player = self.match.get_player(player_id)

        # MatchState.start_turn already increments gold by 1 up to 10.
        self.match.start_turn(player_id, self.round)

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

        if player.shop_frozen:
            return {"type": "ERROR", "code": "ERR_REFRESH_WHILE_FROZEN", "message": "Shop is frozen. Unfreeze first."}
        
        if player.hero.hero_id != "MILLHOUSE_MANASTORM":
            if not self.match.spend_gold(player_id, REFRESH_STORE_COINS):
                return {"type": "ERROR", "code": "ERR_NO_GOLD", "message": "Not enough gold to refresh."}
        else:
            if not self.match.spend_gold(player_id, REFRESH_STORE_COINS_FOR_Millhouse_Manastorm):
                return {"type": "ERROR", "code": "ERR_NO_GOLD", "message": "Not enough gold to refresh."}
        
        self.roll_shop(player_id)

        print("Action was done!\n")
        return {"type": "REFRESH", "gold": player.gold, "shop": list(player.shop)}

    def freeze(self, player_id:str, value: bool = True) -> Dict[str, Any]:
        player = self.match.get_player(player_id)
        player.shop_frozen = bool(value)
        print("Action was done!\n")
        return {"type": "FREEZE", "shop_frozen": player.shop_frozen}

    def buy(self, player_id:str, shop_index: int) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if shop_index < 0 or shop_index >= len(player.shop):
            return {"type": "ERROR", "code": "ERR_INVALI_INDEX", "message": "Invalid shop index."}
        
        if len(player.hand) >= MAX_MINIOS_IN_HAND:
            return {"type": "ERROR", "code": "ERR_INVALI_SLOT", "message": "Hand is full."}
    
        if player.hero.hero_id != "MILLHOUSE_MANASTORM":
            if not self.match.spend_gold(player_id, BUY_MINION_COINS):
                return {"type": "ERROR", "code": "ERR_NO_GOLD", "message": "Not enough gold to buy."}
        else:
            if not self.match.spend_gold(player_id, BUY_MINION_COINS_FOR_Millhouse_Manastorm):
                return {"type": "ERROR", "code": "ERR_NO_GOLD", "message": "Not enough gold to buy."}
        
        card_id = player.shop.pop(shop_index)
        minion = create_minion(card_id)
        player.hand.append(minion)

        print("Action was done!\n")
        return {"type": "BUY", "card_id": card_id, "gold": player.gold, "hand_size": len(player.hand)}

    def play(self, player_id:str, hand_index: int, board_pos: Optional[int] = None) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if hand_index < 0 or hand_index >= len(player.hand):
            return {"type": "ERROR", "code": "ERR_INVALI_INDEX", "message": "Invalid hand index."}
        
        if len(player.board) >= MAX_MINIOS_IN_BOARD:
            return {"type": "ERROR", "code": "ERR_INVALI_SLOT", "message": "Board is full."}

        minion = player.hand.pop(hand_index)

        player.ensure_game_state()
        # GameState.play_minion handles battlecry + global buffs + wrath weaver triggers
        ok = player.game_state.play_minion(minion, position=board_pos)

        if not ok:
            # revert
            player.hand.insert(hand_index, minion)
        
        print("Action was done!\n")
        return {"type": "PLAY", "card_id": minion.card_id, "hp": player.hp, "board_size": len(player.board)}

    def sell(self, player_id:str, board_index: int, refund: int = 1) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if board_index < 0 or board_index >= len(player.board):
            return {"type": "ERROR", "code": "ERR_INVALI_INDEX", "message": "Invalid board index."}
        
        sold = player.board.pop(board_index)
        player.gold = min(10, player.gold + refund)
        
        print("Action was done!\n")
        return {"type": "SELL", "card_id": sold.card_id, "gold": player.gold}

    def upgrade_tavern(self, player_id:str) -> Dict[str, Any]:
        player = self.match.get_player(player_id)

        if player.tavern_tier == 4:
            return {"type": "ERROR", "code": "ERR_MAX_TIER", "message": "Already max tavern tier."}
        
        base_cost_by_tier = {1: 5,
                             2: 7, 
                             3: 8, 
                             4: 9}
        cost = base_cost_by_tier.get(player.tavern_tier)
        if player.hero.hero_id == "MILLHOUSE_MANASTORM": # hero power
            cost += 1

        if not self.match.spend_gold(player_id, cost):
            return {"type": "ERROR", "code": "ERR_NO_GOLD", "message": "Not enough gold to update tavern"}
        
        player.tavern_tier += 1
        # shop stays; next refresh/turn uses higher tier
        print("Action was done!\n")
        return {"type": "UPGRADE", "new_tier": player.tavern_tier, "gold": player.gold, "cost": cost}
    
    def show_tavern_to_player(self, player_id):
        player = self.match.get_player(player_id)
        print(f"\nRound: {self.round} | Tavern Tier: {player.tavern_tier} | Gold: {player.gold} | Frozen: {player.shop_frozen}")
        self.show_shop(player_id)


