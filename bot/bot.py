from sc2.bot_ai import BotAI, Race
from sc2.data import Result
from sc2.ids.unit_typeid import UnitTypeId

MY_PLAYER_ID = 1
OPPONENT_PLAYER_ID = 2

class CompetitiveBot(BotAI):
    NAME: str = "RebelScum"
    """This bot's name"""

    RACE: Race = Race.Terran
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    def __init__(self):
        super().__init__()
        self.enemy_location: Point2 = None
        self.fight_started = False

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")

    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """

        await self._client.debug_create_unit([[UnitTypeId.SUPPLYDEPOT, 1, self.start_location.towards(self.game_info.map_center, 5), MY_PLAYER_ID]])

        if (self.units or self.structures) and (self.enemy_units or self.enemy_structures):
            self.enemy_location = (self.enemy_units + self.enemy_structures).center
            self.fight_started = True

        await self.manage_own_units()

    async def manage_own_units(self):
        for unit in self.units(UnitTypeId.MARINE):
            unit.attack(self.enemy_location)
            # TODO: implement your fight logic here
            # if unit.weapon_cooldown != 0:
            #     unit.move(u.position.towards(self.start_location))
            # else:
            #     unit.attack(self.enemy_location)
            # pass

    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
