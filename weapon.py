import os
from collections import defaultdict

from genshin_data import GenshinData
from stat_block import StatBlock

wep_data = GenshinData.load_weapon_data('resources/genshin_data/genshin_weapon_data.csv')

class Weapon:

    weapon_locations = defaultdict(lambda: list())

    def __init__(self, id, name, lv, ascension, refine):
        self.id = id
        self.name = name
        self.lv = lv
        self.ascension = ascension
        self.refine = refine
        self.awakened = self.ascension >= 2
        self.stat_block = StatBlock({'base_atk': wep_data.loc[name]['ATK'], wep_data.loc[name]['Secondary']: wep_data.loc[name]['Value']})
        self.locations = []

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

    def get_buffs(self):
        return []

    def add_location(self, loc):
        self.locations.append(loc)
        Weapon.weapon_locations[loc] = self