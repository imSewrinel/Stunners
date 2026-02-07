# because can't find the top-level package common
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.match_state import MatchState
from common.hero import Hero
from common.recruit_phase import RecruitPhase


def assert_true(x, msg=""):
    if not x:
        raise AssertionError(msg or "assertion failed")


def test_recruit():
    match = MatchState()
    match.add_player("p1", Hero(None, None, 30, "MILLHOUSE", 0, "test"))

    recruit_phase = RecruitPhase(match)
    player1 = match.players["p1"]

    recruit_phase.start_recruit(player1.player_id)
    print("\nTURN 1 ))")
    recruit_phase.show_shop(player1.player_id)
    assert_true(player1.gold == 3, "gold should be 3 on turn 1")
    assert_true(len(player1.shop) == 3, "shop should have 3 cards")

    print(" ---> buying the first minion of shop:")
    recruit_phase.buy(player1.player_id, 0)
    recruit_phase.show_hand(player1.player_id)
    recruit_phase.show_shop(player1.player_id)
    assert_true(len(player1.hand) == 1, "hand should have 1 after buy")
    assert_true(player1.gold == 0, "gold should be 0 after buy")

    print(" ---> playing the first minion of hand on board:")
    recruit_phase.play(player1.player_id, 0) # not cost any gold
    recruit_phase.show_hand(player1.player_id)
    recruit_phase.show_board(player1.player_id)
    assert_true(len(player1.hand) == 0, "hand should have 0 after play")
    assert_true(len(player1.board) == 1, "board should have 1 after play")

    print("\nTURN 2 ))")
    recruit_phase.start_recruit(player1.player_id)
    recruit_phase.show_shop(player1.player_id)
    assert_true(player1.gold == 4, "gold should be 4 on turn 2")

    print(" ---> selling the first minion of board:")
    recruit_phase.sell(player1.player_id, 0)
    recruit_phase.show_board(player1.player_id)
    assert_true(len(player1.board) == 0, "board should be empty after sell")
    assert_true(player1.gold == 5, "gold should be 5 after sell")

    print(" ---> updating the Tavern Tier:")
    recruit_phase.upgrade_tavern(player1.player_id)
    assert_true(player1.tavern_tier == 2, "tavern_tier should be 2")
    assert_true(player1.gold == 0, "gold should be 0 after upgrade tavern tier 1 to 2")

    print("\nTURN 3 ))")
    recruit_phase.start_recruit(player1.player_id)
    # Shop is updateded after updating tavern tier
    recruit_phase.show_shop(player1.player_id)
    assert_true(len(player1.shop) == 4, "shop should have 4 cards")
    assert_true(player1.gold == 5, "gold should be 5 on turn 3")



def main():
    test_recruit()
    print("ALL TESTS PASSED ✅")

if __name__ == "__main__":
    main()