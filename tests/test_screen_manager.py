import unittest
from core.screen_manager import ScreenManager, ScreenType
from screens.login_screen import LoginScreen
from screens.lobby_screen import LobbyScreen
from screens.game_screen import GameScreen
from screens.result_screen import ResultScreen
from common.hero import Hero
from common.minion import BuzzingVermin


class TestManager(unittest.TestCase):
    def Setup(self):
        self.manager = ScreenManager()
        self.manager.register(ScreenType.LOGIN , LoginScreen)
        self.manager.register(ScreenType.LOBBY , LobbyScreen)
        self.manager.register(ScreenType.GAME , GameScreen)
        self.manager.register(ScreenType.RESULT , ResultScreen)

    def test_login_to_lobby(self):
        self.manager.change_screen(ScreenType.LOGIN)
        self.assertIsInstance(self.manager.current_screen, LoginScreen) 

        self.manager.update()
        self.assertIsInstance(self.manager.current_screen, LobbyScreen)

    def test_lobby_hero_selection(self):
        self.manager.change_screen(ScreenType.LOBBY)

        #رو اینجا دستی انتخاب میکنیم hero


        self.manager.hero = Hero("YOGG", "Yogg-Saron", "Tentacle Gift", 0, "active")

        #میریم به صفحه ی بازی

        self.manager.change_screen(ScreenType.GAME)
        self.assertIsInstance(self.manager.current_screen, GameScreen)
        self.assertEqual(self.manager.hero.hero_id, "YOGG")

    def test_game_add_minion(self):
        self.manager.change_screen(ScreenType.GAME)
        game = self.manager.game_state

        # مینیون اضافه میکنیم
        game.add_to_board(BuzzingVermin())
        self.assertEqual(len(game.board), 1)

    def test_hero_power(self):
        self.manager.hero = Hero("YOGG", "Yogg-Saron", "Tentacle Gift", 0, "active")
        self.manager.ChangeScreen(ScreenType.GAME)

        hero = self.manager.hero
        game = self.manager.game_state

        ok , massage = hero.use_power(match_state=game, player_id=0, target=None)

        self.assertTrue(ok)
        self.assertIn("Hero power", massage)
    def test_screen_flow(self):

        # اینجا از صفحه لاگین میره به لابی بعد گیم بعد ریزالت

        self.manager.ChangeScreen(ScreenType.LOGIN)
        self.manager.update()  # اینجا میره لابی
        self.assertIsInstance(self.manager.current_screen, LobbyScreen)


        # انتخاب هیرو
        self.manager.hero = Hero("YOGG", "Yogg-Saron", "Tentacle Gift", 0, "active")
        self.manager.ChangeScreen(ScreenType.GAME)
        self.assertIsInstance(self.manager.current_screen, GameScreen)

        # رفتن به صفحه نتیجه
        self.manager.ChangeScreen(ScreenType.RESULT)
        self.assertIsInstance(self.manager.current_screen, ResultScreen)

if __name__ == "__main__" :
    unittest.main()