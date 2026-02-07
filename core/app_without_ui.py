from typing import *
from core.event_log import EventLog
from common.match_state import MatchState
from common.hero import Hero
from common.recruit_phase import RecruitPhase
from common.combat_phase import CombatPhase
import random



class Offline_No_UI_App:
    def __init__(self):
        print("_________________Welcome to Hearthstone Battleground_________________\n\n")
        self.match = MatchState()
        # TODO: event log not completed
        self.event_log = EventLog()

        # ------- The client as a main player -------
        self.hero = self.choose_hero()
        self.match.add_player("p1", self.hero) # "p1" is the ID of you

        # ------- System as an enemy -------
        print("You will play offline with the system: \n")
        print("You're hero is", self.hero.hero_id)
        self.enemy_hero = self.get_random_hero()
        self.match.add_player("system", self.enemy_hero)
        print("You're enemy's hero is", self.enemy_hero.hero_id, "\n")

        # ------- Phases of the game -------
        self.recruit_phase = RecruitPhase(self.match)
        self.enemy_recruit_phase = RecruitPhase(self.match)
        self.combat_phase = CombatPhase(self.match)
        print("GOOD LUCK :) \n\n\n")


    def start_the_game(self): # test case for system
        enemy = self.match.get_player("system")

        while (self.match.is_match_done()):
            self.recruit_phase.start_recruit("p1")
            self.recruit_phase.show_tavern_to_player("p1")

            while True:
                print("Choose Your Action: \n(enter 1=buy, 2=play, 3=sell, 4=update, 5=freez, 6=refresh, 7=show tavern, 8=show hand, 9=show board 0=exit)")
                action_num: str = int(input("---> "))
                if action_num == 1:
                    print("Which minion: (enter the index of this minion available in shop)")
                    index: int = int(input("---> "))
                    self.recruit_phase.buy("p1", index) # error handelling in this function
                elif action_num == 2:
                    print("Which minion: (enter the index of this minion available in hand)")
                    index: int = int(input("---> "))
                    self.recruit_phase.play("p1", index)
                elif action_num == 3:
                    print("Which minion: (enter the index of this minion available on board)")
                    index: int = int(input("---> "))
                    self.recruit_phase.sell("p1", index) # error handelling in this function
                elif action_num == 4:
                    self.recruit_phase.upgrade_tavern("p1") # error handelling in this function
                elif action_num == 5:
                    self.recruit_phase.freeze("p1")
                elif action_num == 6: 
                    self.recruit_phase.refresh("p1")
                elif action_num == 7:
                    self.recruit_phase.show_tavern_to_player("p1")
                elif action_num == 8:
                    self.recruit_phase.show_hand("p1")
                elif action_num == 9:
                    self.recruit_phase.show_board("p1")
                elif action_num == 0:
                    break # combat phase
                else:
                    print("!!!Wrong Action, TRY AGAIN!!!\n\n")

            # enemy test case -> recruit, buy and play the first minion of shop
            self.enemy_recruit_phase.start_recruit("system")
            self.enemy_recruit_phase.buy("system", 0)
            self.enemy_recruit_phase.play("system", 0)

            result = self.combat_phase.fight("p1", "system")
            print("___________________________\nThe winner of this round is:", result.winner, "\n___________________________\n")

    def choose_hero(self) -> Hero:
        print("Please Choose your hero:\n(enter 1=YOGG  2=LICH_KING  3=SYLVANAS  4=MILLHOUSE_MANASTORM)\n")
        while (True):
            hero_num: str = input("---> ")
            if hero_num == "1":
                hero = Hero("YOGG", "Yogg-Saron", 30, "Puzzle Box", 0, "active",  uses_per_turn=1)
                return hero
            elif hero_num == "2":
                hero = Hero("LICH_KING", "Lich King", 30, "Reborn Rites", 0, "active", requires_target=True)
                return hero
            elif hero_num == "3":
                hero = Hero("SYLVANAS", "Sylvanas", 30, "Reclaimed Souls ", 0, "active")
                return hero
            elif hero_num == "4":
                hero = Hero("MILLHOUSE_MANASTORM", "Millhouse Manastorm", 30, "Manastorm", 0, "passive")
                return hero
            else:
                print("!!!Wrong Answer, TRY AGAIN!!!\n\n")


    def get_random_hero(self):
        hero_num = random.randint(1, 4)
        if hero_num == 1:
            hero = Hero("YOGG", "Yogg-Saron", 30, "Puzzle Box", 0, "active", uses_per_turn=1)
            return hero
        elif hero_num == 2:
            hero = Hero("LICH_KING", "Lich King", 30, "Reborn Rites", 0, "active", requires_target=True)
            return hero
        elif hero_num == 3:
            hero = Hero("SYLVANAS", "Sylvanas", 30, "Reclaimed Souls ", 0, "active")
            return hero
        elif hero_num == 4:
            hero = Hero("MILLHOUSE_MANASTORM", "Millhouse Manastorm", 30, "Manastorm", 0, "passive")
            return hero

