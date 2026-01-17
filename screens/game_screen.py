from screens.screen_base import Screen
from core.screen_manager import ScreenType
from common.minion import *
import pygame
import time


class Game_screen(Screen):
    def load(self):
        self.last_message = ""
        self.message_time = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                hero = self.manager.hero
                match = self.manager.match_state
                ok, message = hero.use_power(match_state=match, player_id=self.manager.player_id, target=None)
                self.last_message = message
                self.message_time = time.time()
            elif event.key == pygame.K_r:
                self.manager.change_screen(ScreenType.RESULT)

    def update(self):
        # auto-clear message after 3s
        if self.last_message and time.time() - self.message_time > 3:
            self.last_message = ""

    def render(self):
        self.draw_text("GAME", 50, 50, size=40)
        hero_name = self.manager.hero.name if self.manager.hero else "NoHero"
        self.draw_text(f"Hero: {hero_name}", 50, 120)
        self.draw_text("Press H to use hero power, R to result", 50, 160)
        if self.last_message:
            self.draw_text(f"Msg: {self.last_message}", 50, 200, color=(200, 255, 200))



#     def load(self):
#         print("Entering Game Screen...")
#         self.state = self.manager.game_state
#         self.match = self.manager.match_state
#         self.hero = self.manager.hero
#         self.player_id = self.manager.player_id
#         try:
#             self.player = self.match.get_player(self.player_id)
#         except Exception:
#             # No player registered yet
#             self.player = None

#     def update(self):
#         print("\nCommands : summon, damage, board, hero, player, exit")  
#         command = input(">").strip().lower()  
#         if command == "summon" :
#             self.command_summon()
#         elif command == "damage":
#             self.command_damage()
#         elif command == "board":
#             self.state.debug_print_board()
#         elif command == "hero":
#             self.use_hero_power()
#         elif command == "exit":
#             self.manager.change_screen(ScreenType.RESULT)
#         else:
#             print("Unknown command")


#     def command_summon(self):
#         print("Enter card_id to summon")
#         card_id = input("Card ID: ").strip().upper()
#         ok = self.state.summon_minion(card_id)

#         if not ok :
#             print("Could not summon minion")
#             return
#         summoned = self.state.board[-1]
#         self.player.board.append(summoned)
#         print("Summoned: " , summoned)


#     def command_damage(self):
#         try:
#             slot = int(input("Slot index: ")) 
#             dmg = int(input("Damage: ")) 
#         except ValueError:
#             print("Invalid input.") 
#             return
#         self.state.deal_damage_to_slot(slot, dmg)


#     def use_hero_power(self):
#         hero = self.hero
#         if hero.requires_target:
#             if not self.player.board:
#                 print("No minions on your board to target.")
#                 return 
#             print("Your board:")
#             for i, m in enumerate(self.player.board):
#                 print(f"{i}: {m}") 
#             try:
#                 idx = int(input("Target index: ")) 
#             except ValueError:
#                 print("Invalid index.") 
#                 return 
#             if idx < 0 or idx >= len(self.player.board):
#                 print("Invalid index.") 
#                 return 
#             target = self.player.board[idx]
#         else:
#             target = None
#         ok, message = hero.use_power(match_state=self.match, player_id=self.player_id, target=target)
#         print(message)
         
#     def render(self):
#         pass         
                
            



    


















