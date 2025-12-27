from core.screen_base import Screen
from core.screen_manger import ScreenType

class LoginScreen(Screen):
    def update(self):
        print("Login successful.")
        self.manager.ChangeScreen(ScreenType.LOBBY)

    def render(self):
        pass




