import pygame

# Game settings
WIDTH = 900
HEIGHT = 500
CAPTION = "STUNNERS GAME"
FPS = 60


# Player settings
#------------------
# COINS
START_COINS = 3
INCREASE_COINS_PER_TURN = 1
MAX_COINS = 10
BUY_MINION_COINS = 3
BUY_MINION_COINS_FOR_Millhouse_Manastorm = 2
SALE_MINION_COINS = 1
REFRESH_STORE_COINS = 1
REFRESH_STORE_COINS_FOR_Millhouse_Manastorm = 2
FREEZE_COINS = 0
#------------------
# GOLDEN, RECRUIT, DISCOVER
TAVERN_SIZE_BASE_ON_TIRE = {1: 3,
                            2: 4, 
                            3: 4,
                            4: 5}
MAX_MINIOS_IN_HAND = 10
MAX_MINIOS_IN_BOARD = 7


# ANIMATION (ms)
ATTACK_START = 220
DAMAGE_RESOLVE = 120
DEATHRATTLE_TRIGGLE = 300
SUMMON_DELAY = 80
REBORN_SPAWN = 260


# IMAGE PATHS
BASE_IMAGE_PATH = 'assets/'
ALLOWED_IMAGE_EXTS = (".webp", ".png", ".jpg")

# Screens
FONT_CACHE = {}


