from genshin_data import GenshinData
from reactions import Reactions, ReactionTypes


# Characters
def bennett_builder(wep_atk):
    def bennett_buff(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        ratio = 1.12 + .20
        bennett_base_atk = 191.16
        flat_atk += (ratio * (bennett_base_atk + wep_atk))
        return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em
    return bennett_buff


def sucrose_a1(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 50
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def sucrose_a4(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 169.73  # 20% of sucrose em
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def collei_c4(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 60
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


# Artifacts
def thundering_fury_2p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus(0.15, GenshinData.ElementTypes.ELECTRO)
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def thundering_fury_4p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    reaction_bonus.add_bonus(0.40, ReactionTypes.OVERLOAD)
    reaction_bonus.add_bonus(0.40, ReactionTypes.CHARGE)
    reaction_bonus.add_bonus(0.40, ReactionTypes.SCOND)
    reaction_bonus.add_bonus(0.40, ReactionTypes.HBLOOM)
    reaction_bonus.add_bonus(0.20, ReactionTypes.AGG)
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def vv_4p_builder(element):
    def vv_4p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        def_redu.add_bonus(0.4, element)
        return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em
    return vv_4p

def wandererstroupe_2p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 80
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


artifact_buff_quick_add = {
    'ThunderingFury2': thundering_fury_2p,
    'ThunderingFury4': thundering_fury_4p,
    'WanderersTroupe2': wandererstroupe_2p

}


# Weapons
def mistsplitter_builder(stacks):
    def mistsplitter_buff(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        amounts = [0.08, 0.16, 0.28]
        total_boost = 0.12 + amounts[stacks]
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.ELECTRO)
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.PYRO)
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.CRYO)
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.HYDRO)
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.ANEMO)
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.GEO)
        dmg_.add_bonus(total_boost, GenshinData.ElementTypes.DENDRO)
        return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em
    return mistsplitter_buff


#Resonance
def pyro_res(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    atk_ += 0.25
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def cryo_res(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    crit_rate += 0.15
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def geo_res(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus(0.15, GenshinData.ElementTypes.ALL)
    def_redu += 0.2
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em


def dendro_res_builder(after_primary, after_secondary):
    em_bonus = 50
    if after_primary:
        em_bonus += 30
    if after_secondary:
        em_bonus += 20

    def dendro_res(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        em += em_bonus
        return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, em
    return dendro_res
