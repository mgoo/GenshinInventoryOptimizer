from enum import Enum

from genshin_data import GenshinData
from utils import load_json_data

char_data = GenshinData.load_char_data("resources/genshin_data/genshin_char_data_4_1.csv")

class Account:
    def __init__(self, path):
        account_data = load_json_data(path)

        artifacts = account_data["artifacts"]
        self.artifacts = GenshinData.tabulate_artifacts(artifacts)

        weapons = account_data['weapons']
        # TODO get weapon data properly

        self.characters = dict()
        for character in account_data['characters']:
            char_artifact_list = self.artifacts.loc[self.artifacts["location"] == character['key']].to_dict('records')
            char_artifacts = dict()
            for artifact in char_artifact_list:
                artifact = GenshinData.dictionise_row(artifact)
                char_artifacts[artifact['slot']] = artifact

            self.characters[character['key']] = Character(
                character['key'],
                character['level'], character['talent']['auto'], character['talent']['skill'], character['talent']['burst'],
                {'atk': 100, 'atk_': 0.1},  # TODO get proper data
                char_artifacts,
                char_data.loc[character['key']]
            )

class Character:
    def __init__(self, name, level, n_level, skill_level, burst_level, weapon, artifacts, raw_data):
        self.name = name
        self.level = level
        self.n_level = n_level
        self.skill_level = skill_level
        self.burst_level = burst_level
        self.weapon = weapon
        self.artifacts = artifacts

        self._raw_data = raw_data

        self.crit_dmg = GenshinData.char_base_crit_dmg + self.weapon['crit_dmg'] if 'crit_dmg' in self.weapon.keys() else 0
        self.crit_rate = GenshinData.char_base_crit_rate + self.weapon['crit_rate'] if 'crit_rate' in self.weapon.keys() else 0
        # char data
        self.char_atk = raw_data["ATK"]
        self.atk_ = weapon['atk_'] if 'atk_' in weapon.keys() else 0
        self.flat_atk = 0
        self.dmg_ = DmgBonus()
        self.em = 0 + weapon['em'] if 'em' in weapon.keys() else 0

        self.wep_atk = weapon['atk']

        # Character Asscension stats
        if raw_data['Ascension Attributes'] == 'atk_':        self.atk_ += raw_data["Ascension Stat"]
        elif raw_data['Ascension Attributes'] == 'em':        self.em += raw_data["Ascension Stat"]
        elif raw_data['Ascension Attributes'] == 'crit_dmg':  self.crit_dmg += raw_data["Ascension Stat"]
        elif raw_data['Ascension Attributes'] == 'crit_rate': self.crit_rate += raw_data["Ascension Stat"]
        elif raw_data['Ascension Attributes'] in GenshinData.element_types:
            self.dmg_.add_bonus(raw_data["Ascension Stat"], raw_data['Ascension Attributes'])

        # Main stats
        for item in self.artifacts.values():
            if item['main_stat'] == 'atk':         self.flat_atk += item['main_stat_value']
            elif item['main_stat'] == 'atk_':      self.atk_ += item['main_stat_value']
            elif item['main_stat'] == 'em':        self.em += item['main_stat_value']
            elif item['main_stat'] == 'crit_dmg':  self.crit_dmg += item['main_stat_value']
            elif item['main_stat'] == 'crit_rate': self.crit_rate += item['main_stat_value']
            elif item['main_stat'] in GenshinData.element_types:
                self.dmg_.add_bonus(item['main_stat_value'], item['main_stat'])

        # Sub stats
        for item in self.artifacts.values():
            for stat, value in item['sub_stats'].items():
                if stat == 'atk':         self.flat_atk += value
                elif stat == 'atk_':      self.atk_ += value
                elif stat == 'em':        self.em += value
                elif stat == 'crit_dmg':  self.crit_dmg += value
                elif stat == 'crit_rate': self.crit_rate += value

    def rebuild(self, new_artifacts=None, new_weapon=None):
        artifacts = new_artifacts if new_artifacts is not None else self.artifacts
        weapon = new_weapon if new_weapon is not None else self.weapon
        return Character(self.name, self.level, self.n_level, self.skill_level, self.burst_level, weapon, artifacts, self._raw_data)

class Party:

    def __init__(self, char1, char2, char3, char4):
        self.characters = (char1, char2, char3, char4)


class ElementalWrapper:
    def __init__(self):
        self._all = 0
        self._element = dict()
        for elem in GenshinData.element_types:
            self._element[elem] = 0

    def get(self, element):
        if isinstance(element, GenshinData.ElementTypes):
            element = element.value

        assert element != GenshinData.ElementTypes.ALL.value  # Everything should have an element

        return self._element[GenshinData.ElementTypes.ALL.value] + self._element[element]

    def add_bonus(self, amount, type):
        if isinstance(type, GenshinData.ElementTypes):
            type = type.value
        if type == GenshinData.ElementTypes.ALL.value:
            self._all += amount
        elif type in self._element:
            self._element[type] += amount
        else:
            raise Exception("element " + type + "not found")


class DmgTypes(Enum):
    NORMAL = 'n'
    CHARGE = 'c'
    PLUNGE = 'p'
    BURST = 'b'
    SKILL = 's'


class DmgBonus(ElementalWrapper):
    def __init__(self):
        super().__init__()
        self._type = dict()
        for type in DmgTypes:
            self._type[type.value] = 0

    def get(self, element, type=None):
        if isinstance(type, DmgTypes):
            type = type.value
        return super(DmgBonus, self).get(element) + self._type[type]

    def add_bonus(self, amount, type):
        if isinstance(type, DmgTypes):
            type = type.value
        if isinstance(type, GenshinData.ElementTypes):
            type = type.value
        if type == GenshinData.ElementTypes.ALL.value:
            self._all += amount
        elif type in self._element:
            self._element[type] += amount
        elif type in self._type:
            self._type[type] += amount
        else:
            raise Exception("unkown dmg type " + type)