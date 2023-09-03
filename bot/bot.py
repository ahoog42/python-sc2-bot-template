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

        # build scv first time around only
        if iteration == 0:
            await self.build_workers()

        if self.workers.idle:
            await self.distribute_workers();

        await self.build_supply();
        await self.build_barracks();
        await self.train_marines();
        await self.attack_enemy_location();

        #await self.build_barracks()

        if (self.units or self.structures) and (self.enemy_units or self.enemy_structures):
            self.enemy_location = (self.enemy_units + self.enemy_structures).center
            self.fight_started = True

    async def build_workers(self):
        for cc in self.townhalls(UnitTypeId.COMMANDCENTER).ready.idle:
            if self.can_afford(UnitTypeId.SCV):
                cc.train(UnitTypeId.SCV)

    async def expand(self):
        if self.townhalls(UnitTypeId.COMMANDCENTER).amount < 3 and self.can_afford(UnitTypeId.COMMANDCENTER):
            await self.expand_now()

    async def build_supply(self):
        ccs = self.townhalls(UnitTypeId.COMMANDCENTER).ready
        if ccs.exists:
            cc = ccs.first
            if self.supply_left < 4 and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center, 5))
                    # await self.distribute_workers();

    async def train_marines(self):
        #first_barracks = self.townhalls(UnitTypeId.BARRACKS).ready
        #if first_barracks.exists and self.can_afford(UnitTypeId.MARINE):
        self.train(UnitTypeId.MARINE, 1);

    async def build_barracks(self):
        if not self.already_pending(UnitTypeId.BARRACKS):
            #worker = self.select_build_worker()
            ccs = self.townhalls(UnitTypeId.COMMANDCENTER).ready
            if ccs.exists:
                cc = ccs.first
                # Can return None
                #if worker and (await self.can_place(UnitTypeId.BARRACKS, [barracks_placement_position])[0]:
                if self.can_afford(UnitTypeId.BARRACKS) and self.units(UnitTypeId.BARRACKS).amount < 6:
                    await self.build(UnitTypeId.BARRACKS, near=cc);

    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack_enemy_location(self):
        if self.units(UnitTypeId.MARINE).amount > 9:
            #if len(self.known_enemy_units) > 0:
            for s in self.units(UnitTypeId.MARINE).idle:
                #await self.do(s.attack(self.find_target(self.state)))
                self.do(s.attack(self.enemy_start_locations[0]))
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
