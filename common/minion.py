class Minion:
    def __init__(
            self,
            card_id,
            name,
            tier,
            attack,
            health,
            tribe=None,
            keywords=None,
            initial_x=0,
            initial_y=0
        ):
        # Data-only minion (visuals handled by the client/GameManager)
        self.card_id = card_id
        self.name = name
        self.tier = tier
        self.attack = attack
        self.health = health
        self.tribe = tribe
        self.keywords = set(keywords) if keywords else set()

        self.is_golden = False
        self.dead = False

        # برای Hero Power Lich King:
        # فقط برای "کامبت بعدی" به یک مینیون داده می‌شود (UI-ready)
        self.reborn_next_combat = False
        # position for simple client rendering (not required)
        self.pos = (initial_x, initial_y)

    def clone(self):
        """Copy for combat simulation (keeps the same card class/hook behavior)."""
        minion = self.__class__() if self.__class__ is not Minion else Minion(
            self.card_id, self.name, self.tier, self.attack, self.health,
            tribe=self.tribe, keywords=set(self.keywords),
            initial_x=0, initial_y=0
        )
        # Copy dynamic state
        minion.is_golden = getattr(self, "is_golden", False)
        minion.dead = getattr(self, "dead", False)
        minion.reborn_next_combat = getattr(self, "reborn_next_combat", False)
        minion.pos = getattr(self, "pos", (0, 0))
        return minion

    def is_alive(self):
        return self.health > 0 and not self.dead

    def take_damage(self, damage):
        if self.dead:
            return True
        self.health -= damage
        if self.health <= 0:
            self.dead = True
        return self.dead

    def buff(self, attack=0, health=0):
        self.attack += attack
        self.health += health

    # hooks (برای آینده: combat loop / end turn / ...)
    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass

    def after_attack(self, game_state):
        pass

    # رویداد عمومی: “یک مینیون خودی play شد”
    # (برای کارت‌هایی مثل Wrath Weaver که به play شدن بقیه واکنش می‌دهند)
    def on_friendly_minion_played(self, game_state, played_minion):
        pass

    def __repr__(self):
        return f"<Minion {self.name} {self.attack}/{self.health} keywords={self.keywords}>"


# TOKENS

class BeetleToken(Minion):
    def __init__(self):
        super().__init__("BEETLE_TOKEN", "Beetle", 1, 1, 1, tribe="Beast")


class SkeletonToken(Minion):
    def __init__(self):
        super().__init__("SKELETON_TOKEN", "Skeleton", 1, 1, 1, tribe="Undead")


class HandToken(Minion):
    def __init__(self):
        super().__init__("HAND_TOKEN", "Hand", 1, 2, 1, tribe="Undead", keywords={"Reborn"})


# BEETLE BUILD

class BuzzingVermin(Minion):
    def __init__(self):
        super().__init__("BUZZING_VERMIN", "Buzzing Vermin", 1, 1, 1, tribe="Beast", keywords={"Taunt", "Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Buzzing Vermin deathrattle triggers, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class ForestRover(Minion):
    def __init__(self):
        super().__init__("FOREST_ROVER", "Forest Rover", 2, 2, 3, tribe="Beast", keywords={"Battlecry", "Deathrattle"})

    def on_play(self, game_state):
        # فقط Beetle ها در کل بازی +1/+1 می‌گیرند
        game_state.global_card_buffs["BEETLE_TOKEN"]["attack"] += 1
        game_state.global_card_buffs["BEETLE_TOKEN"]["health"] += 1

    def on_deathrattle(self, game_state):
        print("Forest Rover deathrattle triggers, summoning a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class SprightlyScarab(Minion):
    def __init__(self):
        super().__init__("SPRIGHTLY_SCARAB", "Sprightly Scarab", 3, 2, 1, tribe="Beast", keywords={"Deathrattle"})

    def on_play(self, game_state):
        pass
    
    def on_deathrattle(self, game_state):
        pass


class NestSwarmer(Minion):
    def __init__(self):
        super().__init__("NEST_SWARMER", "Nest Swarmer", 5, 6, 6, tribe="Beast", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Nest Swarmer deathrattle triggers, summoning three Beetles...")
        for _ in range(3):
            game_state.summon_minion("BEETLE_TOKEN")


class TurquoiseSkitterer(Minion):
    def __init__(self):
        super().__init__("TURQUOISE_SKITTERER", "Turquoise Skitterer", 4, 2, 4, tribe="Beast", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        game_state.global_card_buffs["BEETLE_TOKEN"]["attack"] += 1
        game_state.global_card_buffs["BEETLE_TOKEN"]["health"] += 2
        print("Turquoise Skitterer deathrattle triggers: Beetles +1/+2, then summon a Beetle...")
        game_state.summon_minion("BEETLE_TOKEN")


class MonstrousMacaw(Minion):
    def __init__(self):
        super().__init__("MONSTROUS_MACAW", "Monstrous Macaw", 3, 4, 3, tribe="Beast")

    def after_attack(self, game_state):
        print("Monstrous Macaw after_attack: triggering left-most friendly Deathrattle...")
        game_state.trigger_leftmost_friendly_deathrattle(exclude_minion=self)


# UNDEAD

class HarmlessBonehead(Minion):
    def __init__(self):
        super().__init__("HARMLESS_BONEHEAD", "Harmless Bonehead", 1, 1, 1, tribe="Undead", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Harmless Bonehead died, summoning two Skeletons...")
        for _ in range(2):
            game_state.summon_minion("SKELETON_TOKEN")


class HandlessForsaken(Minion):
    def __init__(self):
        super().__init__("HANDLESS_FORSAKEN", "Handless Forsaken", 3, 2, 1, tribe="Undead", keywords={"Deathrattle"})

    def on_deathrattle(self, game_state):
        print("Handless Forsaken died, summoning a Hand (2/1) with Reborn...")
        game_state.summon_minion("HAND_TOKEN")


class NerubianDeathswarmer(Minion):
    def __init__(self):
        super().__init__("NERUBIAN_DEATHSWARMER", "Nerubian Deathswarmer", 2, 1, 4, tribe="Undead", keywords={"Battlecry"})

    def on_play(self, game_state):
        # buff دائمی برای Undead های آینده
        game_state.global_tribe_buffs["Undead"]["attack"] += 1

        # اعمال فوری روی Undead های فعلی
        for m in game_state.board:
            if m.tribe == "Undead" and m.is_alive():
                m.buff(attack=1, health=0)

        print("Nerubian Deathswarmer battlecry: all Undead get +1 Attack (permanent).")


class EternalKnight(Minion):
    def __init__(self):
        super().__init__("ETERNAL_KNIGHT", "Eternal Knight", 2, 5, 1, tribe="Undead", keywords={"Battlecry"})

    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass


class EternalSummoner(Minion):
    def __init__(self):
        super().__init__("ETERNAL_SUMMONER", "Eternal Summoner", 6, 8, 1, tribe="Undead", keywords={"Battlecry"})

    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass


class CatacombCrasher(Minion):
    def __init__(self):
        super().__init__("CATACOMB_CRASHER", "Catacomb Crasher", 5, 5, 10, tribe="Undead", keywords={"Battlecry"})

    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass


class TitusRivendare(Minion):
    def __init__(self):
        super().__init__("TITUS_RIVENDARE", "Titus Rivendare", 5, 1, 7, tribe="Undead", keywords={"Battlecry"})

    def on_play(self, game_state):
        pass

    def on_deathrattle(self, game_state):
        pass


# DEMON

class WrathWeaver(Minion):
    """
    After you play a Demon, gain +2/+2 and deal 1 damage to your hero.
    """
    def __init__(self):
        super().__init__("WRATH_WEAVER", "Wrath Weaver", 1, 1, 3, tribe="Demon")

    def on_friendly_minion_played(self, game_state, played_minion):
        # اگر یک Demon play شد (حتی خودِ Weaver)، تریگر می‌خورد
        if played_minion.tribe == "Demon":
            self.buff(attack=2, health=2)
            game_state.deal_hero_damage(1)
            print("Wrath Weaver triggers: +2/+2 and hero takes 1 damage.")


class ImpMama(Minion):
    def __init__(self):
        super().__init__("IMP_MAMA", "Imp Mama", 6, 6, 10, tribe="Demon")

    def on_friendly_minion_played(self, game_state, played_minion):
            pass


class FalseImplicator(Minion):
    def __init__(self):
        super().__init__("FALSE_IMPLICATOR", "False Implicator", 3, 1, 1, tribe="Demon")

    def on_friendly_minion_played(self, game_state, played_minion):
            pass
    

class FuriousDriver(Minion):
    def __init__(self):
        super().__init__("FURIOUS_DRIVER", "Furious Driver", 5, 3, 3, tribe="Demon")

    def on_friendly_minion_played(self, game_state, played_minion):
            pass
    

class FamishedFelbat(Minion):
    def __init__(self):
        super().__init__("FAMISHED_FELBAT", "Famished Felbat", 6, 9, 5, tribe="Demon")

    def on_friendly_minion_played(self, game_state, played_minion):
            pass
    





# --------- Minion factory (card_id -> class) ---------
MINION_FACTORY = {
    # tokens
    "BEETLE_TOKEN": BeetleToken,
    "SKELETON_TOKEN": SkeletonToken,
    "HAND_TOKEN": HandToken,

    # beetles
    "BUZZING_VERMIN": BuzzingVermin,
    "FOREST_ROVER": ForestRover,
    "SPRIGHTLY_SCARAB": SprightlyScarab,
    "NEST_SWARMER": NestSwarmer,
    "TURQUOISE_SKITTERER": TurquoiseSkitterer,
    "MONSTROUS_MACAW": MonstrousMacaw,

    # undeads
    "HARMLESS_BONEHEAD": HarmlessBonehead,
    "HANDLESS_FORSAKEN": HandlessForsaken,
    "NERUBIAN_DEATHSWARMER": NerubianDeathswarmer,
    "ETERNAL_KNIGHT": EternalKnight,
    "ETERNAL_SUMMONER": EternalSummoner,
    "CATACOMB_CRASHER": CatacombCrasher,
    "TITUS_RIVENDARE": TitusRivendare,

    # demons
    "WRATH_WEAVER": WrathWeaver,
    "IMP_MAMA": ImpMama,
    "FALSE_IMPLICATOR": FalseImplicator,
    "FURIOUS_DRIVER": FuriousDriver,
    "FAMISHED_FELBAT": FamishedFelbat,
}


def create_minion(card_id: str):
    cls = MINION_FACTORY.get(card_id)
    if cls is None:
        raise ValueError(f"Unknown card_id: {card_id}")
    return cls()