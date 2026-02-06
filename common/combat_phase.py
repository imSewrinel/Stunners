from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import random
from common.match_state import MatchState
from common.player import PlayerState
from common.minion import Minion


@dataclass
class CombatResult:
    winner: str | None  # player_id or None
    rounds: int


# ------------- Combat class -------------
class CombatPhaseError(Exception):
    pass

class CombatPhase:
    def __init__(self, match: MatchState, rng: random.Random | None = None):
        self.match = match
        self.rng = rng or random.Random()

    def is_living(self, board: List[Minion]) -> bool:
        for minion in board:
            if minion.health > 0:
                return True
        return False

    def _pick_target_index(self, defenders: List[Minion]) -> int:
        taunts = [i for i, m in enumerate(defenders) if getattr(m, "taunt", False) and m.health > 0]
        candidates = taunts if taunts else [i for i, m in enumerate(defenders) if m.health > 0]
        return self.rng.choice(candidates)

    def fight(self, player1_id:str, player2_id:str) -> CombatResult:
        player1 = self.match.get_player(player1_id)
        player2 = self.match.get_player(player2_id)

        player1.ensure_game_state()
        player2.ensure_game_state()

        # Deep copy boards (combat should not mutate recruit boards directly)
        board1 = [minion.clone() for minion in player1.board]
        board2 = [minion.clone() for minion in player2.board]

        attacker_is_player1 = self.rng.choice([True, False])
        rounds = 0

        while self.is_living(board1) and self.is_living(board2):
            rounds += 1
            if rounds > 500:
                raise CombatPhaseError("Combat exceeded safety limit (possible infinite loop).")

            atk_board = board1 if attacker_is_player1 else board2
            def_board = board2 if attacker_is_player1 else board1

            # pick first living attacker (left-to-right)
            attacker_idx = next((i for i, minion in enumerate(atk_board) if minion.health > 0), None)
            if attacker_idx is None:
                break

            defender_idx = self._pick_target_index(def_board)

            attacker = atk_board[attacker_idx]
            defender = def_board[defender_idx]

            # Attacker hits defender
            print("=== Minion (", attacker.name, ") hits minion (", defender.name, ") ===")
            defender.health -= attacker.attack
            # Check if defender is dead or not
            if defender.health <= 0:
                print("    Minion (", defender.name, ") is dead now!")
                def_board.pop(defender_idx)
            else:
            # Defender hits back if alive
                print("=== Minion (", defender.name, ") hits back minion (", attacker.name, ") ===")
                attacker.health -= defender.attack
                # Check if attacker is dead or not
                if attacker.health <= 0:
                    print("    Minion (", attacker.name, ") is dead now!")
                    atk_board.pop(attacker_idx)

            # TODO: game_state board should be updated

            attacker_is_player1 = not attacker_is_player1

        player1_alive = self.is_living(board1)
        player2_alive = self.is_living(board2)

        if player1_alive and not player2_alive:
            return CombatResult(winner=player1.player_id, rounds=rounds)
        
        if player2_alive and not player1_alive:
            return CombatResult(winner=player2.player_id, rounds=rounds)
        
        return CombatResult(winner=None, rounds=rounds)
