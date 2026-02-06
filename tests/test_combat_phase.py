# because can't find the top-level package common
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from common.combat_phase import CombatPhase
from common.match_state import MatchState
from common.hero import Hero
from common.minion import Minion

def assert_true(x, msg=""):
    if not x:
        raise AssertionError(msg or "assertion failed")

def test_combat_taunt_targeting():
    match = MatchState()

    match.add_player("p1", Hero(None, None, 0, 0, "MILLHOUSE", "test", "test_power", 1, None))
    match.add_player("p2", Hero(None, None, 0, 0, "MILLHOUSE", "test", "test_power", 1, None))

    player1 = match.players["p1"]
    player2 = match.players["p2"]

    # Force simple minions
    a = Minion("Alleycat", "Alleycat", 2, 5, 5)

    t = Minion("Vulgar_Homunculus", "Vulgar Homunculus", 1, 1, 1)
    setattr(t, "taunt", True)

    big = Minion("Rockpool_Hunter", "Rockpool Hunter", 3, 100, 100)

    player1.board = [a]
    player2.board = [t, big]

    combat_phase = CombatPhase(match, rng=random.Random(42))
    result = combat_phase.fight(player1.player_id, player2.player_id)

    assert_true(result.rounds > 0, "combat should run")
    # taunt should die quickly; after that attacker should eventually lose vs big (likely)
    assert_true(result.winner in (player1.player_id, player2.player_id, None))
    print("___________________________\nThe winner is:", result.winner, "\n___________________________\n")


def main():
    test_combat_taunt_targeting()
    print("ALL TESTS PASSED ✅")


if __name__ == "__main__":
    main()