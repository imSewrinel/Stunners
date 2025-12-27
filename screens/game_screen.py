from core.screen_base import Screen
from core.screen_manager import ScreenType
from common.minion import *

class GameScreen(Screen):
    def load(self):
        print("Entering Game Screen...")
        self.state = self.manager.game_state
        self.match = self.manager.match_state
        self.hero = self.manager.hero
        self.player_id = self.manager.player_id
        self.player = self.match.get_player(self.player_id)


    def update(self):
        print("\nCommands : summon, damage, board, hero, player, exit")  
        command = input(">").strip().lower()  
        if command == "summon" :
            self.command_summon()
        elif command == "damage":
            self.command_damage()
        elif command == "board":
            self.state.debug_print_board()
        elif command == "hero":
            self.use_hero_power()
        elif command == "exit":
            self.manager.ChangeScreen(ScreenType.RESULT)
        else:
            print("Unknown command")


    def command_summon(self):
        print("Enter card_id to summon")
        card_id = input("Card ID: ").strip().upper()
        ok = self.state.summon_minion(card_id)

        if not ok :
            print("Could not summon minion")
            return
        summoned = self.state.board[-1]
        self.player.board.append(summoned)
        print("Summoned : " , summoned)


    def command_damage(sefl):
        try:

            slot = int(input("Slot index: ")) 
            dmg = int(input("Damage: ")) 
        except ValueError:
            print("Invalid input.") 
        return
        self.state.deal_damage_to_slot(slot, dmg)


    def use_hero_power(self):
        hero = self.hero

        if hero.requires_target:
            if not self.player.board:
                print("No minions on your board to target.")
                return 
            print("Your board:")
            for i, m in enumerate(self.player.board):
                print(f"{i}: {m}") 
            try:
                idx = int(input("Target index: ")) 
            except ValueError:
                print("Invalid index.") 
                return 
            if idx < 0 or idx >= len(self.player.board):
                print("Invalid index.") 
                return 
            target = self.player.board[idx]
        else:
            target = None


        ok, massage = hero.use_power(matc_state=self.match ,player_id = self.player_id ,target=target)
        print(massage) 
    def render(self):
        pass         
                
            



    


















