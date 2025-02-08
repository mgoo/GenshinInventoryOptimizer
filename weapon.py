import os
from collections import defaultdict
from abc import ABC, abstractmethod

from genshin_data import GenshinData
from stat_block import StatBlock

wep_data = GenshinData.load_weapon_data('resources/genshin_data/genshin_weapon_data.csv')

class Weapon(ABC):

    weapon_locations = defaultdict(lambda: list())

    @abstractmethod
    def __init__(self, id, lv, ascension, refine):
        self.id = id
        self.lv = lv
        self.ascension = ascension
        self.refine = refine
        self.awakened = self.ascension >= 2
        self.locations = []

        # By default make the weapon name the same as the class name. This will need to get overridden in the generic case
        self.name = self.__class__.__name__

    def get_img(self):
        wep_path = os.path.join('static', 'assets', 'weapons', self.name)
        if os.path.isdir(wep_path):
            imgs = [filename for filename in os.listdir(wep_path) if filename != 'index.ts']
            awake_img = None
            sleep_img = None
            for img in imgs:
                if 'Awakened' in img:
                    awake_img = img
                else:
                    sleep_img = img

            final_img = None
            if awake_img is not None and (self.awakened or sleep_img is None):
                final_img = awake_img
            if sleep_img is not None and (not self.awakened or awake_img is None):
                final_img = sleep_img
        else:
            final_img = None
        if final_img is None:
            return 'img/noimg.jpg'
        return 'assets/weapons/' + self.name + '/' + final_img

    @abstractmethod
    def get_buffs(self):
        raise Exception('Abstract Method')

    def add_location(self, loc):
        self.locations.append(loc)
        Weapon.weapon_locations[loc] = self


class GenericWeapon(Weapon):

    def __init__(self, id, name, lv, ascension, refine):
        super().__init__(id, lv, ascension, refine)

        self.name = name

        self.base_atk = wep_data.loc[name]['ATK']
        self.secondary = wep_data.loc[name]['Secondary']
        self.secondary_value = wep_data.loc[name]['Value']
        self.weapon_class = wep_data.loc[name]['Weapon Type']

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        return StatBlock({})


class CrimsonMoonsSemblance(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 674
        self.secondary = 'crit_rate'
        self.secondary_value = .165
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})


class StaffoftheScarletSands(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 541
        self.secondary = 'crit_rate'
        self.secondary_value = .441
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class CalamityQueller(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 741
        self.secondary = 'atk_'
        self.secondary_value = '16.5%'
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class EngulfingLightning(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'er_'
        self.secondary_value = .551
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class PrimordialJadeWingedSpear(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 674
        self.secondary = 'crit_rate'
        self.secondary_value = .221
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SkywardSpine(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 674
        self.secondary = 'er_'
        self.secondary_value = .368
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class StaffOfHoma(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'crit_dmg'
        self.secondary_value = .662
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class VortexVanquisher(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'atk_'
        self.secondary_value = .496
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class TheCatch(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'er_'
        self.secondary_value = .459
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class BlackcliffPole(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'crit_dmg'
        self.secondary_value = .551
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class CrescentPike(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'phys_'
        self.secondary_value = .345
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class Deathmatch(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'crit_rate'
        self.secondary_value = .368
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class DragonsBane(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'em'
        self.secondary_value = 221
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class DragonspineSpear(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'phys_'
        self.secondary_value = .69
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class FavoniusLance(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'er_'
        self.secondary_value = .306
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class KitainCrossSpear(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'em'
        self.secondary_value = 110
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class Lithicspear(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'atk_'
        self.secondary_value = .276
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class PrototypeStarglitter(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'er_'
        self.secondary_value = .459
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class RoyalSpear(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'atk_'
        self.secondary_value = .276
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class WavebreakersFin(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 620
        self.secondary = 'atk_'
        self.secondary_value = .138
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class MoonPiercer(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'em'
        self.secondary_value = 110
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class MissiveWindspear(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'atk_'
        self.secondary_value = .414
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class BalladOfTheFjords(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'crit_rate'
        self.secondary_value = .276
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class RightfulReward(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'hp_'
        self.secondary_value = .276
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class ProspectorsDrill(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'atk_'
        self.secondary_value = .276
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class DialoguesOfTheDesertSages(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'hp_'
        self.secondary_value = .414
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class BlackTassel(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 354
        self.secondary = 'hp_'
        self.secondary_value = .469
        self.weapon_class = 'polearm'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class UrakuMisugiri(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 542
        self.secondary = 'crit_dmg'
        self.secondary_value = .882
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SplendorofTranquilWaters(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 542
        self.secondary = 'crit_dmg'
        self.secondary_value = .882
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class LightOfFoliarIncision(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 542
        self.secondary = 'crit_dmg'
        self.secondary_value = .882
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class KeyofKhajNisut(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 541
        self.secondary = 'hp_'
        self.secondary_value = .661
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class HaranTsukishiroFutsu(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'crit_rate'
        self.secondary_value = .331
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class AquilaFavonia(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 674
        self.secondary = 'phys_'
        self.secondary_value = .413
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class FreedomSworn(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'em'
        self.secondary_value = 198
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class MistsplitterReforged(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 674
        self.secondary = 'crit_dmg'
        self.secondary_value = .441
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        stacks = 2
        if stacks == 3:
            stacks =  3.5
        stack_buff = stacks * (0.06 + self.refine * 0.02)
        return StatBlock({'elem_': 0.09 + 0.03 * self.refine + stack_buff})

class PrimordialJadeCutter(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 542
        self.secondary = 'crit_rate'
        self.secondary_value = .441
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SkywardBlade(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'er_'
        self.secondary_value = .551
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SummitShaper(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'atk_'
        self.secondary_value = .496
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class ToukabouShigure(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'em'
        self.secondary_value = 165
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class WolfFang(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'crit_rate'
        self.secondary_value = .276
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        skill_stacks = 2
        burst_stacks = 2
        return StatBlock({
            's_': 0.12 + 0.04 * self.refine,
            'b_': 0.12 + 0.04 * self.refine,
            's_crit_rate': (0.015 + 0.005 * self.refine) * skill_stacks,
            'b_crit_rate': (0.015 + 0.005 * self.refine) * burst_stacks
        })


class FinaleoftheDeep(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'atk_'
        self.secondary_value = .276
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class CrossingofFleuveCendre(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'er_'
        self.secondary_value = .46
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class AmenomaKageuchi(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'atk_'
        self.secondary_value = .551
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class BlackcliffLongsword(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'crit_dmg'
        self.secondary_value = .368
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class FavoniusSword(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'er_'
        self.secondary_value = .613
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class FesteringDesire(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'er_'
        self.secondary_value = .459
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class IronSting(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'em'
        self.secondary_value = 165
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class LionsRoar(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'atk_'
        self.secondary_value = .413
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class PrototypeRancour(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'phys_'
        self.secondary_value = .345
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class RoyalLongsword(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'atk_'
        self.secondary_value = .413
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SacrificialSword(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'er_'
        self.secondary_value = .613
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SwordofDescension(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 440
        self.secondary = 'atk_'
        self.secondary_value = .352
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class TheAlleyFlash(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 620
        self.secondary = 'em'
        self.secondary_value = 55
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class TheBlackSword(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'crit_rate'
        self.secondary_value = .276
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class TheFlute(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'atk_'
        self.secondary_value = .413
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class CinnabarSpindle(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'def_'
        self.secondary_value = .69
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class KagotsurubeIsshin(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'atk_'
        self.secondary_value = .413
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SapwoodBlade(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'er_'
        self.secondary_value = .306
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class XiphosMoonlight(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'em'
        self.secondary_value = 165
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SwordOfNarzissenkreuz(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'atk_'
        self.secondary_value = .413
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class FleuveCendreFerryman(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'er_'
        self.secondary_value = .46
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class HarbingerOfDawn(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 401
        self.secondary = 'crit_dmg'
        self.secondary_value = .469
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class TheDockhandsAssistant(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 510
        self.secondary = 'hp_'
        self.secondary_value = .414
        self.weapon_class = 'sword'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class TheFirstGreatMagic(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'crit_dmg'
        self.secondary_value = .662
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class HuntersPath(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 541
        self.secondary = 'crit_rate'
        self.secondary_value = .441
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class AquaSimulacra(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 542
        self.secondary = 'crit_dmg'
        self.secondary_value = .882
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class AmosBow(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'atk_'
        self.secondary_value = .496
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class ElegyfortheEnd(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'er_'
        self.secondary_value = .551
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class PolarStar(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'crit_rate'
        self.secondary_value = .331
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class SkywardHarp(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 674
        self.secondary = 'crit_rate'
        self.secondary_value = .221
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class ThunderingPulse(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 608
        self.secondary = 'crit_dmg'
        self.secondary_value = .662
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class AlleyHunter(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'atk_'
        self.secondary_value = .276
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class BlackcliffWarbow(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 565
        self.secondary = 'crit_dmg'
        self.secondary_value = .368
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class CompoundBow(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'phys_'
        self.secondary_value = .69
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})

class FavoniusWarbow(Weapon):
    def __init__(self, id, lv=90, ascension=5, refine=1):
        super().__init__(id, lv, ascension, refine)
        self.base_atk = 454
        self.secondary = 'er_'
        self.secondary_value = .613
        self.weapon_class = 'bow'

        self.stat_block = StatBlock({
            'base_atk': self.base_atk,
            self.secondary: self.secondary_value
        })

    def get_buffs(self):
        # TODO not implemented
        return StatBlock({})