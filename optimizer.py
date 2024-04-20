import collections

from buffs import *
from characters import ElementalWrapper, DmgBonus, DmgTypes, Character
from reactions import Reactions, ReactionBonuses
from genshin_data import GenshinData


class Optimizer:

    def __init__(self):
        pass

    def get_value(self, args):
        """
        Gets the damage a character would do with a specific artifact
        Users only one param as this is made to be run in parallel
        :param args:
        :return:
        """
        option = args['option']
        character = args['character']
        account = args['account']

        new_artifacts = character.artifacts.copy()
        new_artifacts[option['slot']] = option
        character = character.rebuild(new_artifacts=new_artifacts)

        return self.calc_dmg(character, account)

    def calc_dmg(self, character, account):
        """
        Calculates a damage number that is used as a heuristic for how good an artifact is
        :param character:
        :param account
        :return:
        """

        buffs = [
            vv_4p_builder(GenshinData.ElementTypes.ELECTRO), sucrose_a1, sucrose_a4_builder(account.characters['Sucrose']),
            mistsplitter_builder(2)
        ]

        artifact_sets = collections.Counter([item['set'] for item in character.artifacts.values()])
        for set, number in artifact_sets.items():
            if number >= 2:
                buffs.append(artifact_buff_quick_add[set + '2'])
            if number >= 4:
                buffs.append(artifact_buff_quick_add[set + '4'])

        n = self.char_dmg(.81, character, DmgTypes.NORMAL, GenshinData.ElementTypes.ELECTRO , buffs=buffs)
        c_1_agg = self.char_dmg(1.51, character, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO, reaction=Reactions.AGG, buffs=buffs)
        c_1 = self.char_dmg(1.51, character, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO, buffs=buffs)
        c_2 = self.char_dmg(1.51, character, DmgTypes.CHARGE, GenshinData.ElementTypes.ELECTRO, buffs=buffs)

        return (n + c_1_agg + c_2) + (n + c_1 + c_2)

    def char_dmg(self,
            talent_, char, atk_type, element, reaction=Reactions.NONE,
            buffs=None
    ):
        char_atk = char.char_atk
        wep_atk = char.wep_atk
        atk_ = char.atk_
        flat_atk = char.flat_atk
        dmg_ = char.dmg_
        crit_rate = char.crit_rate
        crit_dmg = char.crit_dmg
        em = char.em

        if buffs is None:
            buffs = []

        def_redu = ElementalWrapper()
        reaction_bonus = ReactionBonuses()

        base_atk = (char_atk + wep_atk)
        for buff in buffs:
            talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em = buff(
                talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus,
                def_redu)
        return reaction.calc_dmg(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, atk_type, element, reaction_bonus, def_redu)


