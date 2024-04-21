import collections

from buffs import *
from characters import ElementalWrapper, DmgBonus, DmgTypes, Character, character_cache
from reactions import Reactions, ReactionBonuses
from genshin_data import GenshinData


def atk_scaler_builder(scale):
    def atk_scale(total_atk, em, hp, defence):
        return scale * total_atk
    return atk_scale


def em_scaler_builder(scale):
    def em_scale(total_atk, em, hp, defence):
        return scale * em
    return em_scale


def hp_scaler_builder(scale):
    def hp_scale(total_atk, em, hp, defence):
        return scale * hp
    return hp_scale


def defence_scaler_builder(scale):
    def defence_scale(total_atk, em, hp, defence):
        return scale * defence
    return defence_scale


class Optimizer:

    def __init__(self):
        pass

    def get_value(self, option, character, account):
        """
        Gets the damage a character would do with a specific artifact
        Users only one param as this is made to be run in parallel
        :param args:
        :return:
        """
        new_artifacts = character.artifacts.copy()
        new_artifacts[option['slot']] = option
        character = character.rebuild(new_artifacts=new_artifacts)

        return self.calc_dmg(character, account)

    # For Keqing!!
    def calc_dmg(self, character, account):
        """
        Calculates a damage number that is used as a heuristic for how good an artifact is
        :param character:
        :param account
        :return:
        """

        buffs = [
            vv_4p_builder(GenshinData.ElementTypes.ELECTRO), sucrose_a1, sucrose_a4_builder(character_cache['Sucrose']),
            collei_c4,
            mistsplitter_builder(2)
        ]

        artifact_sets = collections.Counter([item['set'] for item in character.artifacts.values()])
        for set, number in artifact_sets.items():
            if number >= 2:
                buffs.append(artifact_buff_quick_add[set + '2'])
            if number >= 4:
                buffs.append(artifact_buff_quick_add[set + '4'])


        n = self.char_dmg([atk_scaler_builder(.81)], character, DmgTypes.NORMAL, GenshinData.ElementTypes.ELECTRO , buffs=buffs, reaction=Reactions.AGG)
        c_1_agg = self.char_dmg([atk_scaler_builder(1.51)], character, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO, buffs=buffs, reaction=Reactions.AGG)
        c_2 = self.char_dmg([atk_scaler_builder(1.70)], character, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO, buffs=buffs)

        e = self.char_dmg([atk_scaler_builder(.9072)], character, DmgTypes.SKILL, GenshinData.ElementTypes.ELECTRO, buffs=buffs)
        e_recast = self.char_dmg([atk_scaler_builder(3.024)], character, DmgTypes.SKILL, GenshinData.ElementTypes.ELECTRO, buffs=buffs)

        q_init = self.char_dmg([atk_scaler_builder(1.584)], character, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, buffs=buffs, reaction=Reactions.AGG)
        q_c = self.char_dmg([atk_scaler_builder(0.4328)], character, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, buffs=buffs)
        q_c_agg = self.char_dmg([atk_scaler_builder(0.4328)], character, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, buffs=buffs, reaction=Reactions.AGG)
        q_final = self.char_dmg([atk_scaler_builder(3.3984)], character, DmgTypes.BURST, GenshinData.ElementTypes.ELECTRO, buffs=buffs, reaction=Reactions.AGG)

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
    #     return q1 * 4 + q1_spread * 2 + q2 * 4 + q2_spread * 2 + c + c1 * 4 + c + c1 * 4 + c + c1 * 4

    def char_dmg(self,
            talent_, char: Character, atk_type, element, reaction=Reactions.NONE,
            buffs=None
    ):
        if buffs is None:
            buffs = []

        talent_, flat_dmg, dmg_, def_redu, reaction_bonus = char.apply_buffs(buffs, reaction, talent_)

        total_hp = char.char_hp * (1 + char.hp_) + char.flat_hp
        total_def = char.char_def * (1 + char.def_) + char.flat_def
        total_atk = (char.char_atk + char.wep_atk) * (1 + char.atk_) + char.flat_atk
        return reaction.calc_dmg(talent_, total_atk, total_hp, total_def, flat_dmg, char.crit_rate, char.crit_dmg, dmg_, char.em, atk_type, element, reaction_bonus, def_redu)


