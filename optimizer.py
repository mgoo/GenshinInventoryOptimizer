from buffs import *
from reactions import Reactions
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
        fixed_artifacts = args['fixed_artifacts']
        weapon = args['weapon']
        char_data = args['char_data']

        assert option['slot'] not in fixed_artifacts
        fixed_artifacts[option['slot']] = option

        return self.calc_dmg(fixed_artifacts, weapon, char_data)

    def calc_dmg(self, char_artifacts, weapon, char_data):
        """
        Calculates a damage number that is used as a heuristic for how good an artifact is
        :param character:
        :param char_artifacts:
        :param weapon:
        :param char_data:
        :return:
        """
        crit_dmg = GenshinData.char_base_crit_dmg + weapon['crit_dmg'] if 'crit_dmg' in weapon.keys() else 0
        crit_rate = GenshinData.char_base_crit_rate + weapon['crit_rate'] if 'crit_rate' in weapon.keys() else 0
        # char data
        char_atk = char_data["ATK"]
        atk_ = weapon['atk_'] if 'atk_' in weapon.keys() else 0
        flat_atk = 0
        dmg_ = 0
        em = 0 + weapon['em'] if 'em' in weapon.keys() else 0

        atk_wep = weapon['atk']

        # Character Asscension stats
        if char_data['Ascension Attributes'] == 'atk_':        atk_ += char_data["Ascension Stat"]
        elif char_data['Ascension Attributes'] == 'electro_':  dmg_ += char_data["Ascension Stat"]  # TODO Handle different type of damage % bonus
        elif char_data['Ascension Attributes'] == 'em':        em += char_data["Ascension Stat"]
        elif char_data['Ascension Attributes'] == 'crit_dmg':  crit_dmg += char_data["Ascension Stat"]
        elif char_data['Ascension Attributes'] == 'crit_rate': crit_rate += char_data["Ascension Stat"]

        # Main stats
        for item in char_artifacts.values():
            if item['main_stat'] == 'atk':         flat_atk += item['main_stat_value']
            elif item['main_stat'] == 'atk_':      atk_ += item['main_stat_value']
            elif item['main_stat'] == 'electro_':  dmg_ += item['main_stat_value']  # TODO Handle different type of damage % bonus
            elif item['main_stat'] == 'em':        em += item['main_stat_value']
            elif item['main_stat'] == 'crit_dmg':  crit_dmg += item['main_stat_value']
            elif item['main_stat'] == 'crit_rate': crit_rate += item['main_stat_value']

        # Sub stats
        for item in char_artifacts.values():
            for stat, value in item['sub_stats'].items():
                if stat == 'atk':         flat_atk += value
                elif stat == 'atk_':      atk_ += value
                elif stat == 'em':        em += value
                elif stat == 'crit_dmg':  crit_dmg += value
                elif stat == 'crit_rate': crit_rate += value

        buffs = [
            vv_4p, sucrose_a1, sucrose_a4,
            thundering_fury_2p, thundering_fury_4p,
            mistsplitter_builder(2)
        ]
        n = self.char_dmg(.81, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, buffs=buffs)
        c_1_agg = self.char_dmg(1.51, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, reaction=Reactions.AGG, buffs=buffs)
        c_1 = self.char_dmg(1.51, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, buffs=buffs)
        c_2 = self.char_dmg(1.51, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, buffs=buffs)

        return (n + c_1_agg + c_2) + (n + c_1 + c_2)

    def char_dmg(self,
            talent_,
            char_atk, wep_atk, atk_, flat_atk,
            dmg_bonus_,
            crit_rate, crit_dmg,
            em, reaction=Reactions.NONE, reaction_bonus=0.0,
            def_redu=0.0,
            buffs=None
    ):
        if buffs is None:
            buffs = []

        base_atk = (char_atk + wep_atk)
        for buff in buffs:
            talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu = buff(
                talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus,
                def_redu)
        return reaction.calc_dmg(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction_bonus,
                                 def_redu)


