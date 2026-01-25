from screens.screen_base import Screen
from core.screen_manager import ScreenType
import pygame


class LoginScreen(Screen):
    def load(self):
        self.msg = "Press ENTER to Login"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.manager.change_screen(ScreenType.LOBBY) # access from Screen (base) class 

    def update(self):
        pass

    def render(self):
        self.draw_text("LOGIN SCREEN", 50, 50, size=40)
        self.draw_text(self.msg, 50, 120)



