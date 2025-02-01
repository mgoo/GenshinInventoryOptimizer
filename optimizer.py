from functools import reduce

import autograd.numpy as np
from autograd import grad, elementwise_grad
import collections

from buffs import *
from characters import DmgTypes, Character, character_cache, Account
from reactions import Reactions, ReactionBonuses
from genshin_data import GenshinData
from stat_block import StatBlock


class OptimizerStatBlock(StatBlock):
    parameter_names = GenshinData.stat_names

    @classmethod
    def from_stat_block(cls, stat_block: StatBlock):
        return cls(stat_block._stats)

    def to_stat_block(self):
        return StatBlock({key: self[key] for key in self.parameter_names})

    def __init__(self, values: dict):
        super().__init__(values)
        self._stats = np.array([values[stat] if stat in values else 0 for stat in self.parameter_names], dtype=np.float64)

    def get_idx(self, stat):
        return self.parameter_names.index(stat)

    def __getitem__(self, item):
        return self._stats[self.get_idx(item)]

    def total_atk(self):
        return (self._stats[self.get_idx('base_atk')] * (1 + self._stats[self.get_idx('atk_')])) + self._stats[self.get_idx('atk')]

    def total_def(self):
        return (self._stats[self.get_idx('base_def')] * (1 + self._stats[self.get_idx('def_')])) + self._stats[self.get_idx('def')]

    def total_hp(self):
        return (self._stats[self.get_idx('base_hp')] * (1 + self._stats[self.get_idx('hp_')])) + self._stats[self.get_idx('hp')]

    def get_non_zero(self):
        raise Exception('not yet implemented')

    def add(self, stat, value):
        new_block = OptimizerStatBlock({stat: value})
        return self + new_block

    def __add__(self, other):
        if isinstance(other, OptimizerStatBlock):
            new_block = OptimizerStatBlock({})
            new_block._stats = self._stats + other._stats
            return new_block
        elif isinstance(other, StatBlock):
            raise Exception('not yet implemented')
        raise Exception('not accepted type')

    def __sub__(self, other):
        new_block = OptimizerStatBlock({})
        new_block._stats = self._stats - other._stats
        return new_block

    def __copy__(self):
        new_block = OptimizerStatBlock({})
        new_block._stats = self._stats.copy()
        return new_block

    def as_array(self):
        return self._stats


def atk_scaler_builder(scale):
    def atk_scale(stat_block):
        return scale * stat_block.total_atk()
    return atk_scale


def em_scaler_builder(scale):
    def em_scale(stat_block):
        return scale * stat_block['em']
    return em_scale


def hp_scaler_builder(scale):
    def hp_scale(stat_block):
        return scale * stat_block.total_hp()
    return hp_scale


def defence_scaler_builder(scale):
    def defence_scale(stat_block):
        return scale * stat_block.total_def()
    return defence_scale


# For Keqing!!
def calc_dmg(stats, account):

    # artifact_sets = collections.Counter([item['set'] for item in character.artifacts.values()])
    # for set, number in artifact_sets.items():
    #     if number >= 2:
    #         buffs.append(artifact_buff_quick_add[set + '2'])
    #     if number >= 4:
    #         buffs.append(artifact_buff_quick_add[set + '4'])


    buffs = [
        bennett_builder(account.characters['Bennett'], c1=True)
    ]

    n =        char_dmg([atk_scaler_builder(.81)], stats, buffs, DmgTypes.NORMAL, GenshinData.ElementTypes.ELECTRO , reaction=Reactions.AGG)
    c_1_agg =  char_dmg([atk_scaler_builder(1.51)], stats, buffs, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO, reaction=Reactions.AGG)
    c_2 =      char_dmg([atk_scaler_builder(1.70)], stats, buffs, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO)

    e =        char_dmg([atk_scaler_builder(.9072)], stats, buffs, DmgTypes.SKILL, GenshinData.ElementTypes.ELECTRO)
    e_recast = char_dmg([atk_scaler_builder(3.024)], stats, buffs, DmgTypes.SKILL, GenshinData.ElementTypes.ELECTRO)

    q_init =   char_dmg([atk_scaler_builder(1.584)], stats, buffs, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, reaction=Reactions.AGG)
    q_c =      char_dmg([atk_scaler_builder(0.4328)], stats, buffs, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO)
    q_c_agg =  char_dmg([atk_scaler_builder(0.4328)], stats, buffs, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, reaction=Reactions.AGG)
    q_final =  char_dmg([atk_scaler_builder(3.3984)], stats, buffs, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, reaction=Reactions.AGG)

    return e + q_init + q_c * 6 + q_c_agg * 2 + q_final + e_recast + n + c_1_agg + c_2 + n + c_1_agg + c_2 + e + e_recast + n + c_1_agg + c_2 + n + c_1_agg + c_2

# For Alhatham!!!!
# def calc_dmg(self, character, account):
#     """
#     Calculates a damage number that is used as a heuristic for how good an artifact is
#     :param character:
#     :param account
#     :return:
#     """
#
#     buffs = [
#         nahida_a1_builder(account.characters['Nahida']), thousand_dreams_builder(same=True), deepwood_4p
#     ]
#
#     artifact_buff_quick_add['GildedDreams4'] = gildeddreams_4p_builder(same=1, diff=2)
#     artifact_sets = collections.Counter([item['set'] for item in character.artifacts.values()])
#     for set, number in artifact_sets.items():
#         if number >= 2:
#             buffs.append(artifact_buff_quick_add[set + '2'])
#         if number >= 4:
#             buffs.append(artifact_buff_quick_add[set + '4'])
#
#     q = self.char_dmg(
#         [atk_scaler_builder(2.1888), em_scaler_builder(1.751)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs, reaction=Reactions.SPREAD
#     )
#     e = self.char_dmg(
#         [atk_scaler_builder(3.4848), em_scaler_builder(2.7878)],
#         character, DmgTypes.SKILL, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#     m1 = self.char_dmg(
#         [atk_scaler_builder(1.2096), em_scaler_builder(2.4192)],
#         character, DmgTypes.SKILL, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#     m2 = self.char_dmg(
#         [atk_scaler_builder(2 * 1.2096), em_scaler_builder(2 * 2.4192)],
#         character, DmgTypes.SKILL, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#     m3 = self.char_dmg(
#         [atk_scaler_builder(3 * 1.2096), em_scaler_builder(3 * 2.4192)],
#         character, DmgTypes.SKILL, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#     n1 = self.char_dmg(
#         [atk_scaler_builder(.979)],
#         character, DmgTypes.NORMAL, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs, reaction=Reactions.SPREAD
#     )
#     n2 = self.char_dmg(
#         [atk_scaler_builder(1.0032)],
#         character, DmgTypes.NORMAL, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#
#     return q + e + n1 + n2 + m1 + n1 + n2 + m2 + n1 + n2 + m3

# For Tighnari!!
# def calc_dmg(self, character, account):
#     """
#     Calculates a damage number that is used as a heuristic for how good an artifact is
#     :param character:
#     :param account
#     :return:
#     """
#
#     buffs = [
#         nahida_a1_builder(account.characters['Nahida']), thousand_dreams_builder(same=True), deepwood_4p,
#         tighnari_c1, tighnari_c2, tighnari_a4_builder(character), tighnari_a1
#
#     ]
#
#     artifact_buff_quick_add['GildedDreams4'] = gildeddreams_4p_builder(same=1, diff=2)
#     artifact_sets = collections.Counter([item['set'] for item in character.artifacts.values()])
#     for set, number in artifact_sets.items():
#         if number >= 2:
#             buffs.append(artifact_buff_quick_add[set + '2'])
#         if number >= 4:
#             buffs.append(artifact_buff_quick_add[set + '4'])
#
#     q1 = self.char_dmg(
#         [atk_scaler_builder(1.0012)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#     q1_spread = self.char_dmg(
#         [atk_scaler_builder(1.0012)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs, reaction=Reactions.SPREAD
#     )
#     q2 = self.char_dmg(
#         [atk_scaler_builder(1.2236)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#     q2_spread = self.char_dmg(
#         [atk_scaler_builder(1.2236)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs, reaction=Reactions.SPREAD
#     )
#     c = self.char_dmg(
#         [atk_scaler_builder(1.5696)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs, reaction=Reactions.SPREAD
#     )
#     c1 = self.char_dmg(
#         [atk_scaler_builder(0.6948)],
#         character, DmgTypes.BURST, GenshinData.ElementTypes.DENDRO,
#         buffs=buffs
#     )
#
#     return q1 * 4 + q1_spread * 2 + q2 * 4 + q2_spread * 2 + c + c1 * 4 + c + c1 * 4 + c + c1 *

def char_dmg(talent_, stat_block, buffs, atk_type, element, reaction=Reactions.NONE):
    # TODO calculate buffs
    return reaction.calc_dmg(talent_, stat_block, atk_type, element)

if __name__ == '__main__':
    account = Account("resources/account_data/genshinData_GOOD_2024_04_22_20_23.json")
    character = account.characters['KukiShinobu']
    weapons = [wep for wep in account.weapons.values()]

    char_stats = OptimizerStatBlock.from_stat_block(character.stat_block).as_array()
    artifact_stats = OptimizerStatBlock.from_stat_block(reduce(lambda c, n: c + n, [arti.total_stat_boost() for arti in character.artifacts.values()], StatBlock({}))).as_array()
    weapons_stats = np.array([OptimizerStatBlock.from_stat_block(wep.stat_block).as_array() for wep in weapons], dtype=np.float64)

    weights = np.array([1 for _ in range(weapons_stats.shape[0])], dtype=np.float64)

    def forward(weights):
        e_weights = np.exp(weights - np.max(weights))
        final_weights = e_weights / e_weights.sum()

        final_weapons_stats = np.multiply(final_weights[:, None], weapons_stats)
        final_weapon_stats = np.sum(final_weapons_stats, axis=0)

        stats = char_stats + artifact_stats + final_weapon_stats

        block = OptimizerStatBlock({})
        block._stats = stats

        return calc_dmg(block, account)

    grad_func = elementwise_grad(forward)
    lr = 0.1
    epochs = 5

    for epoch in range(epochs):
        grad = grad_func(weights)
        weights = weights + lr * grad

    best_weapon = np.argmax(weights)
    print(weapons[best_weapon].name)


