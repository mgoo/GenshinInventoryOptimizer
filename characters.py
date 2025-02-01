import os
import re
from enum import Enum
import copy

from genshin_data import GenshinData
from reactions import ReactionBonuses, Reactions
from stat_block import StatBlock
from utils import load_json_data

from artifact import Artifact
from weapon import Weapon

char_data = GenshinData.load_char_data('resources/genshin_data/genshin_char_data_4_1.csv')


character_cache = dict()


class Account:
    def __init__(self, path):
        account_data = load_json_data(path)

        artifacts = account_data["artifacts"]
        self.artifacts = {}
        for raw_artifact in artifacts:
            self.artifacts[raw_artifact["id"]] = Artifact.from_raw(raw_artifact)

        weapons = account_data['weapons']
        self.weapons = {}
        for raw_wep in weapons:
            weapon = Weapon(
                raw_wep['id'], raw_wep['key'],
                raw_wep['level'], raw_wep['ascension'], raw_wep['refinement'],
            )
            self.weapons[weapon.id] = weapon
            if raw_wep['location'] != '':
                weapon.add_location(raw_wep['location'])

        self.characters = dict()
        for character in account_data['characters']:
            self.characters[character['key']] = Character(
                character['key'],
                character['level'], character['talent']['auto'], character['talent']['skill'], character['talent']['burst'],
                Weapon.weapon_locations[character['key']],
                Artifact.artifact_locations[character['key']],
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

        self._raw_data = raw_data

        self.stat_block = StatBlock({
            'base_atk': raw_data["ATK"],
            'base_hp': raw_data["HP"],
            'base_def': raw_data["DEF"],
            'crit_rate': GenshinData.char_base_crit_rate,
            'crit_dmg': GenshinData.char_base_crit_dmg
        }) + StatBlock({
            raw_data['Ascension Attributes']: raw_data["Ascension Stat"]
        })

        self.artifacts = {
            'flower': None,
            'plume': None,
            'sands': None,
            'goblet': None,
            'circlet': None
        }
        for artifact in artifacts:
            self.equip(artifact)

    def get_stats(self, buffs=list()):
        stat_block = self.stat_block + self.weapon.stat_block
        for artifact in self.artifacts.values():
            if artifact is not None:
                stat_block += artifact.total_stat_boost()
        # for buff in buffs:
        #     stat_block = buff(
        #         talent_, stat_block
        #     )
        return stat_block

    def unequip(self, slot):
        # TODO remove set bonus??
        self.artifacts.pop(slot)

    def equip(self, artifact: 'Artifact'):
        # Check if there is an existing artifact in the slot
        if self.artifacts[artifact.slot_key] is not None:
            # if the existing artifact has the same id then dont do anything
            if artifact.id == self.artifacts[artifact.slot_key].id:
                return
            self.unequip(artifact.slot_key)

        # TODO handle set bonus??
        self.artifacts[artifact.slot_key] = artifact


class Party:

    def __init__(self, char1, char2, char3, char4):
        self.characters = (char1, char2, char3, char4)


class DmgTypes(Enum):
    NORMAL = 'n'
    CHARGE = 'c'
    PLUNGE = 'p'
    BURST = 'b'
    SKILL = 's'



