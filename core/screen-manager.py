from enum import Enum
from common.game_state import GameState
from common.match_state import MatchState

class ScreenType(Enum):
    LOGIN = "login"
    LOBBY = "lobby"
    GAME = "game"
    RESULT = "result"

class ScreenManager:
    def __init__(self):
        self.current_screen = None
        self.registry = {}
         # تو این قسمت ذخیره میشن Heroو GameState

        self.game_state = GameState()
        self.match_state = MatchState()
        self.hero = None
        self.player_id = 0

def register(self , screen_type , screen_class):
    self.registry[screen_type] = screen_class

def ChangeScreen(self , screen_type):
    if self.current_screen:
        self.current_screen.unload()
    screen_class = self.registry[screen_type]
    self.current_screen = screen_class(self)
    self.current_screen.load()

def update(self):
    if self.current_screen:
        self.current_screen.update()

def render(self):
    if self.current_screen:
        self.current_screen.render()


