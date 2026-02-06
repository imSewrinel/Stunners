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


def test_recruit_buy_play_sell():
    match = MatchState()
    match.add_player("p1", Hero(None, None, 0, 0, "MILLHOUSE", "test", "test_power", 1, None))

    recruit_phase = RecruitPhase(match)
    player1 = match.players["p1"]

    recruit_phase.start_recruit(player1.player_id)
    assert_true(player1.gold == 3, "gold should be 3 on turn 1")
    assert_true(len(player1.shop) == 3, "shop should have 3 cards")

    recruit_phase.buy(player1.player_id, 0)
    assert_true(len(player1.hand) == 1, "hand should have 1 after buy")
    assert_true(player1.gold == 0, "gold should be 0 after buy")

    recruit_phase.play(player1.player_id, 0) # not cost any gold
    assert_true(len(player1.hand) == 0, "hand should have 0 after play")
    assert_true(len(player1.board) == 1, "board should have 1 after play")

    recruit_phase.start_recruit(player1.player_id, 2)
    assert_true(player1.gold == 1, "gold should be 1 on turn 2 after buying on turn 1")

    # Wrong order of phases just for testing "recruit_phase.sell()"
    recruit_phase.start_recruit(player1.player_id, 3)
    assert_true(player1.gold == 2, "gold should be 2 on turn 3 after turn 2")

    recruit_phase.start_recruit(player1.player_id, 4)
    assert_true(player1.gold == 3, "gold should be 3 on turn 4 after turn 3")

    recruit_phase.buy(player1.player_id, 0)
    assert_true(len(player1.hand) == 1, "hand should have 1 after buy")
    assert_true(player1.gold == 0, "gold should be 0 after buy")

    recruit_phase.sell(player1.player_id, 0)
    assert_true(len(player1.hand) == 0, "board should be empty after sell")
    assert_true(player1.gold == 1, "gold should be 1 after sell")

    # Wrong order of phases just for testing "recruit_phase.sell()"
    recruit_phase.start_recruit(player1.player_id, 5)
    assert_true(player1.gold == 2, "gold should be 2 on turn 5 after buying and selling on turn 4")

    recruit_phase.start_recruit(player1.player_id, 6)
    assert_true(player1.gold == 3, "gold should be 3 on turn 6 after turn 5")

    recruit_phase.start_recruit(player1.player_id, 7)
    assert_true(player1.gold == 4, "gold should be 4 on turn 7 after turn 6")

    recruit_phase.start_recruit(player1.player_id, 8)
    assert_true(player1.gold == 5, "gold should be 5 on turn 8 after turn 7")
    assert_true(player1.tavern_tier == 1, "tavern_tier should be 1")

    recruit_phase.upgrade_tavern(player1.player_id)
    assert_true(player1.tavern_tier == 2, "tavern_tier should be 2")
    assert_true(player1.gold == 0, "gold should be 0 after upgrade tavern tier 1 to 2")


def main():
    test_recruit_buy_play_sell()
    print("ALL TESTS PASSED ✅")

if __name__ == "__main__":
    main()