# because can't find the top-level package common
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.game_state import GameState
from common.minion import BuzzingVermin

if __name__ == "__main__":
    gs = GameState()

    gs.add_to_board(BuzzingVermin())
    gs.debug_print_board()

    print("\n--- Deal huge damage to slot 0 ---")
    gs.deal_damage_to_slot(0, 999)

    gs.debug_print_board()


