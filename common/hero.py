class Hero:
    def __init__(
        self,
        hero_id,
        name,
        power_name,
        power_cost,
        power_type,          # "active" یا "passive"
        requires_target=False,
        uses_per_turn=0
    ):
        self.hero_id = hero_id
        self.name = name
        self.power_name = power_name
        self.power_cost = power_cost
        self.power_type = power_type
        self.requires_target = requires_target
        self.uses_per_turn = uses_per_turn

    def __repr__(self):
        return f"<Hero {self.name} | Power: {self.power_name}>"

