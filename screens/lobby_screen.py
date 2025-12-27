from core.screen_base import Screen
from core.screen_manager import ScreenType
from common.hero import Hero

class LobbyScreen(Screen):
    def update(self):
        print("Choose a hero : YOGG , LICH_KING , SYLVANAS")
        hero_id = input("> ").strip().upper()

        if hero_id == "YOGG" :
            hero = Hero("YOGG" , "Yogg_Saron" , "Tentacle Gift" ,0,"active")
        elif hero_id == "LICH_KING" :
            hero = Hero("LICH_KING" , "Lich king" , "Reborn Blessing" ,0,"active" , requires_target=True)
        elif hero_id == "SYLVANAS" : 
            hero = Hero("SYLVANAS" , "Sylvanas" , "Death Buff" ,0,"active")
        else:
            print("Invalid hero!")  
            return

        self.manager.hero = hero    #saved in ScreenManager
        player_id = self.manager.player_id   #currently 0
        self.manager.match_state.add_player(player_id , hero)
        self.manager.mathc_state.start_turn(player_id)  #starts player's turn
        self.manager.ChangeScreen(ScreenType.GAME)

    def render(self):
        pass   



                
