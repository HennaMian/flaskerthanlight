"""Creates Models for SpaceTrader Game"""
import random
import math
from enum import Enum
from spacetrader import db

class Player(db.Model):
    """Creates Player class based on database"""
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(16), nullable=False)
    pilotskill = db.Column(db.Integer, nullable=False)
    fighterskill = db.Column(db.Integer, nullable=False)
    merchantskill = db.Column(db.Integer, nullable=False)
    engineerskill = db.Column(db.Integer, nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Float, nullable=False)
    curr_region = db.Column(db.String(16), nullable=False)
    market_items = {}

    def __init__(self, pname, pilotskill, fighterskill, merchantskill,
                 engineerskill, credits, money, curr_region):
        self.pname = pname
        self.pilotskill = pilotskill
        self.fighterskill = fighterskill
        self.merchantskill = merchantskill
        self.engineerskill = engineerskill
        self.credits = credits
        self.money = money
        self.curr_region = curr_region

    def buy_prices(self, mskill, tech_l):
        """Defines buying prices for player"""
        prices_per_unit = {}
        bppr = 0.5
        if tech_l == TechLevel.PRE_AG:
            prices_per_unit.update({"Food" : bppr, "Weapons" : bppr, "Wood" : bppr,
                                    "Fur" : bppr})
        elif tech_l == TechLevel.AGRICULTURE:
            prices_per_unit.update({"Food" : bppr*2, "Weapons" : bppr*2,
                                    "Wood" : bppr*2, "Fur" : bppr*2, "Medicine" : bppr*2})
        elif tech_l == TechLevel.MEDIEVAL:
            prices_per_unit.update({"Food" : bppr*2, "Weapons" : bppr*2, "Wood" : bppr*4,
                                    "Fur" : bppr*3, "Medicine" : bppr*4, "Metal" : bppr*4})
        elif tech_l == TechLevel.RENAISSANCE:
            prices_per_unit.update({"Food" : bppr*3, "Weapons" : bppr*4, "Wood" : bppr*6,
                                    "Fur" : bppr*4, "Medicine" : bppr*8, "Metal" : bppr*8,
                                    "Silver" : bppr*100})
        elif tech_l == TechLevel.INDUSTRIAL:
            prices_per_unit.update({"Food" : bppr*3, "Weapons" : bppr*5, "Wood" : bppr*8,
                                    "Fur" : bppr*5, "Medicine" : bppr*16, "Metal" : bppr*12,
                                    "Silver" : bppr*100, "Spices" : bppr*8})
        elif tech_l == TechLevel.MODERN:
            prices_per_unit.update({"Food" : bppr*4, "Weapons" : bppr*6, "Wood" : bppr*10,
                                    "Fur" : bppr*5, "Medicine" : bppr*32, "Metal" : bppr*16,
                                    "Silver" : bppr*120, "Spices" : bppr*10, "Gold" : bppr*180})
        elif tech_l == TechLevel.FUTURISTIC:
            prices_per_unit.update({"Food" : bppr*4, "Weapons" : bppr*8, "Wood" : bppr*12,
                                    "Fur" : bppr*5, "Medicine" : bppr*64, "Metal" : bppr*20,
                                    "Silver" : bppr*140, "Spices" : bppr*12, "Gold" : bppr*200,
                                    "Computers" : bppr*200})

        for key, val in prices_per_unit.items():
            prices_per_unit[key] = round(val/math.sqrt(mskill), 2)

        return prices_per_unit

    def sell_prices(self, mskill, tech_l):
        """Defines selling prices for player"""
        prices_per_unit = {}
        bppr = 0.5
        if tech_l == TechLevel.PRE_AG:
            prices_per_unit.update({"Food" : bppr, "Weapons" : bppr, "Wood" : bppr, "Fur" : bppr})
        elif tech_l == TechLevel.AGRICULTURE:
            prices_per_unit.update({"Food" : bppr*2, "Weapons" : bppr*2,
                                    "Wood" : bppr*2, "Fur" : bppr*2, "Medicine" : bppr*2})
        elif tech_l == TechLevel.MEDIEVAL:
            prices_per_unit.update({"Food" : bppr*2, "Weapons" : bppr*2, "Wood" : bppr*4,
                                    "Fur" : bppr*3, "Medicine" : bppr*4, "Metal" : bppr*4})
        elif tech_l == TechLevel.RENAISSANCE:
            prices_per_unit.update({"Food" : bppr*3, "Weapons" : bppr*4, "Wood" : bppr*6,
                                    "Fur" : bppr*4, "Medicine" : bppr*8, "Metal" : bppr*8,
                                    "Silver" : bppr*100})
        elif tech_l == TechLevel.INDUSTRIAL:
            prices_per_unit.update({"Food" : bppr*3, "Weapons" : bppr*5, "Wood" : bppr*8,
                                    "Fur" : bppr*5, "Medicine" : bppr*16, "Metal" : bppr*12,
                                    "Silver" : bppr*100, "Spices" : bppr*8})
        elif tech_l == TechLevel.MODERN:
            prices_per_unit.update({"Food" : bppr*4, "Weapons" : bppr*6, "Wood" : bppr*10,
                                    "Fur" : bppr*5, "Medicine" : bppr*32, "Metal" : bppr*16,
                                    "Silver" : bppr*120, "Spices" : bppr*10, "Gold" : bppr*180})
        elif tech_l == TechLevel.FUTURISTIC:
            prices_per_unit.update({"Food" : bppr*4, "Weapons" : bppr*8, "Wood" : bppr*12,
                                    "Fur" : bppr*5, "Medicine" : bppr*64, "Metal" : bppr*20,
                                    "Silver" : bppr*140, "Spices" : bppr*12, "Gold" : bppr*200,
                                    "Computers" : bppr*200})

        for key, val in prices_per_unit.items():
            prices_per_unit[key] = round(val*math.sqrt(mskill), 2)

        return prices_per_unit


    def __repr__(self):
        """Represents the Player in the Database"""
        return ("Player('{0}', '{1}', '{2}', '{3}',"
                "'{4}', '{5}', '{6}', '{7}')".format(self.pname, self.pilotskill,
                                                     self.fighterskill,
                                                     self.merchantskill,
                                                     self.engineerskill,
                                                     self.credits, self.money,
                                                     self.curr_region))

class TechLevel(Enum):
    """Defines Tech Level Enum"""
    PRE_AG = 1
    AGRICULTURE = 2
    MEDIEVAL = 3
    RENAISSANCE = 4
    INDUSTRIAL = 5
    MODERN = 6
    FUTURISTIC = 7

class Market(db.Model):
    """Defines Market for each region"""
    id = db.Column(db.Integer, primary_key=True)
    mtype = db.Column(db.String(), nullable=False)

    def __init__(self, mtype):
        self.mtype = mtype

    def dummy_method(self):
        """Dummy Method"""
        print("dummy")

    def __repr__(self):
        return "Market('{0}')".format(self.mtype)


class Region(db.Model):
    """Creates Region class based on database"""
    id = db.Column(db.Integer, primary_key=True)
    rname = db.Column(db.String(16), nullable=False)
    x_coor = db.Column(db.Integer, nullable=False)
    y_coor = db.Column(db.Integer, nullable=False)
    techlevel = db.Column(db.Enum(TechLevel), nullable=False)

    def __init__(self, rname, x_coor, y_coor, techlevel):
        self.rname = rname
        self.x_coor = x_coor
        self.y_coor = y_coor
        self.techlevel = techlevel

    def generate_market(self, items):
        """Defines each Market's inventory based on techlevel"""
        if self.techlevel == TechLevel.PRE_AG:
            items.update({"Food" : 700, "Weapons" : 700, "Wood" : 700, "Fur" : 700})
        elif self.techlevel == TechLevel.AGRICULTURE:
            items.update({"Food" : 600, "Weapons" : 600,
                          "Wood" : 600, "Fur" : 600, "Medicine" : 600})
        elif self.techlevel == TechLevel.MEDIEVAL:
            items.update({"Food" : 500, "Weapons" : 500, "Wood" : 500,
                          "Fur" : 500, "Medicine" : 500, "Metal" : 500})
        elif self.techlevel == TechLevel.RENAISSANCE:
            items.update({"Food" : 400, "Weapons" : 400, "Wood" : 400, "Fur" : 400,
                          "Medicine" : 400, "Metal" : 400, "Silver" : 400})
        elif self.techlevel == TechLevel.INDUSTRIAL:
            items.update({"Food" : 300, "Weapons" : 300, "Wood" : 300, "Fur" : 300,
                          "Medicine" : 300, "Metal" : 300, "Silver" : 300, "Spices" : 300})
        elif self.techlevel == TechLevel.MODERN:
            items.update({"Food" : 200, "Weapons" : 200, "Wood" : 200, "Fur" : 200,
                          "Medicine" : 200, "Metal" : 200, "Silver" : 200, "Spices" : 200,
                          "Gold" : 200})
        elif self.techlevel == TechLevel.FUTURISTIC:
            items.update({"Food" : 100, "Weapons" : 100, "Wood" : 100, "Fur" : 100,
                          "Medicine" : 100, "Metal" : 100, "Silver" : 100, "Spices" : 100,
                          "Gold" : 100, "Computers" : 100})
        return items

    def add_item(self, type_name, items):
        items.update({type_name : 1})
        return items
        
    def add_price(self, type_name, diff, prices):
        if diff == "Easy":
            prices.update({type_name : 1200})
        elif diff == "Medium":
            prices.update({type_name : 600})
        else:
            prices.update({type_name : 150})

        return prices

    def __repr__(self):
        return "Region('{0}', '{1}', '{2}', '{3}')".format(self.rname, self.x_coor,
                                                           self.y_coor, self.techlevel)


class Game(db.Model):
    """Creates Game class based on database"""
    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.String(10), nullable=False)

    def __init__(self, pname, pilotskill, fighterskill, merchantskill,
                 engineerskill, credits, difficulty=None):
        self.difficulty = difficulty
        money = (pilotskill + fighterskill + merchantskill + engineerskill) * 10
        self.start_game()
        rand = random.randrange(0, 10)
        player = Player(pname, pilotskill, fighterskill, merchantskill, engineerskill,
                        credits, money, Universe.regions[rand].rname)
        db.session.add(player)
        db.session.commit()

    def start_game(self):
        """Sets events in motion to start game"""
        universe = Universe(reg_1="Ego", reg_2="Asgard", reg_3="Earth",
                            reg_4="Sakaar", reg_5="Vormir", reg_6="Xandar",
                            reg_7="Morag", reg_8="Titan", reg_9="Knowhere", reg_10="Nidavellir")
        stypes = ["Starship", "Jet", "Wasp", "Ladybug"]
        s_typ = random.choice(stypes)
        carg_s = 600
        fuel_c = 100
        heal = 100
        ship = Ship(stype=s_typ, cargospace=carg_s, fuelcapacity=fuel_c, health=heal)
        db.session.add(universe)
        db.session.commit()
        db.session.add(ship)
        db.session.commit()

    def __repr__(self):
        return "Game('{0}')".format(self.difficulty)

class Ship(db.Model):
    """Creates Player class based on database"""

    id = db.Column(db.Integer, primary_key=True)
    stype = db.Column(db.String(), nullable=False)
    cargospace = db.Column(db.Integer, nullable=False)
    fuelcapacity = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, nullable=False)

    def __init__(self, stype, cargospace, fuelcapacity, health):
        self.stype = stype
        self.cargospace = cargospace
        self.fuelcapacity = fuelcapacity
        self.health = health

    def refuel(self, curr_fuel, requested_fuel):
        """Refuels Ship"""
        fuel_to_fill = requested_fuel - curr_fuel
        fuel_cost = fuel_to_fill * 1.5
        return fuel_cost

    def repair(self, eskill):
        """Repairs Ship"""
        repair_cost = 150 / eskill
        return repair_cost

    def __repr__(self):
        return "Ship('{0}', '{1}', '{2}', '{3}')".format(self.stype, self.cargospace,
                                                         self.fuelcapacity, self.health)

class NPC(db.Model):
    """Creates NPC class based on database"""
    id = db.Column(db.Integer, primary_key=True)
    ctype = db.Column(db.String(), nullable=False)

    def __init__(self, ctype):
        self.ctype = ctype

    def dummy_method(self):
        """Dummy Method"""
        print("dummy")

    def __repr__(self):
        return "NPC('{0}')".format(self.ctype)


class Universe(db.Model):
    """Creates Universe class based on database"""

    id = db.Column(db.Integer, primary_key=True)
    reg_1 = db.Column(db.String(), nullable=False)
    reg_2 = db.Column(db.String(), nullable=False)
    reg_3 = db.Column(db.String(), nullable=False)
    reg_4 = db.Column(db.String(), nullable=False)
    reg_5 = db.Column(db.String(), nullable=False)
    reg_6 = db.Column(db.String(), nullable=False)
    reg_7 = db.Column(db.String(), nullable=False)
    reg_8 = db.Column(db.String(), nullable=False)
    reg_9 = db.Column(db.String(), nullable=False)
    reg_10 = db.Column(db.String(), nullable=False)

    region_names = []
    regions = []
    curr_coords_x = []
    curr_coords_y = []
    market_types = {}

    def __init__(self, reg_1, reg_2, reg_3, reg_4, reg_5,
                 reg_6, reg_7, reg_8, reg_9, reg_10):
        self.reg_1 = reg_1
        self.reg_2 = reg_2
        self.reg_3 = reg_3
        self.reg_4 = reg_4
        self.reg_5 = reg_5
        self.reg_6 = reg_6
        self.reg_7 = reg_7
        self.reg_8 = reg_8
        self.reg_9 = reg_9
        self.reg_10 = reg_10
        Universe.region_names.extend([reg_1, reg_2, reg_3, reg_4, reg_5,
                                      reg_6, reg_7, reg_8, reg_9, reg_10])
        self.create_regions()

    def check_coordinates(self, x_coor, y_coor, curr_coords_x, curr_coords_y):
        """Makes sure coordinates are not within 5 of each other."""
        for i in range(len(curr_coords_x)):
            if abs(x_coor - curr_coords_x[i]) <= 5:
                return False
            elif abs(y_coor - curr_coords_y[i]) <= 5:
                return False
        return True

    def dist_between_regions(self, x_coor1, y_coor1, x_coor2, y_coor2):
        """Calculates distance between regions"""
        squared = ((x_coor2 - x_coor1)**2) + ((y_coor2 - y_coor1)**2)
        return math.sqrt(squared)

    def create_regions(self):
        """Creates Regions"""
        for region_r in Universe.region_names:
            randx = random.randrange(-200, 201)
            randy = random.randrange(-200, 201)
            while not self.check_coordinates(randx, randy, Universe.curr_coords_x,
                                             Universe.curr_coords_y):
                randx = random.randrange(-200, 201)
                randy = random.randrange(-200, 201)
            Universe.curr_coords_x.append(randx)
            Universe.curr_coords_y.append(randy)
            reg = Region(region_r, randx, randy, random.choice(list(TechLevel)))
            Universe.regions.append(reg)
            db.session.add(reg)
            db.session.commit()

        mtypes = ["Food", "Weapons", "Wood", "Fur", "Medicine",
                  "Metal", "Silver", "Spices", "Gold", "Computers"]
        for mtype in mtypes:
            market = Market(mtype)
            db.session.add(market)
            db.session.commit()
            Universe.market_types.update({mtype : random.randint(10, 31)})

    def __repr__(self):
        return (
            "Universe('{0}', '{1}', '{2}', '{3}', '{4}', "
            "'{5}', '{6}', '{7}', '{8}', '{9}')".format(self.reg_1, self.reg_2,
                                                        self.reg_3, self.reg_4,
                                                        self.reg_5,
                                                        self.reg_6, self.reg_7,
                                                        self.reg_8, self.reg_9,
                                                        self.reg_10))
