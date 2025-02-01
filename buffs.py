import autograd.numpy as np

from characters import DmgTypes, Character
from genshin_data import GenshinData
from optimizer import OptimizerStatBlock
from reactions import Reactions
from stat_block import StatBlock


# Characters
def bennett_builder(bennett: Character, c1=False):
    def bennett_buff(stat_block: OptimizerStatBlock):
        ratio = 1.12  # TODO assumes lv 12
        if c1:
            ratio += 0.2
        stat_block = stat_block.add('atk', ratio * (bennett.stat_block['base_atk'] + bennett.weapon.stat_block['base_atk']))
        return stat_block
    return bennett_buff


def sucrose_a1(stat_block: OptimizerStatBlock):
    return stat_block.add('em', 50)


def sucrose_a4_builder(sucrose: Character, buffs=list()):
    def sucrose_a4(stat_block: OptimizerStatBlock):
        return stat_block.add('em', sucrose.get_stats(buffs)['em'] * 0.2)
    return sucrose_a4


def collei_c4(stat_block: OptimizerStatBlock):
    return stat_block.add('em', 60)


def nahida_a1_builder(highest_em_char, buffs=list()):
    def nahida_a1(stat_block: OptimizerStatBlock):
        return stat_block.add('em', min(highest_em_char.get_stats(buffs)['em'] * 0.25, 250))
    return nahida_a1


def alhaitham_a4_builder(alhaitham):
    def alhaitham_a4(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        bonus = 0.001 * alhaitham.em
        dmg_.add_bonus_enum(bonus, DmgTypes.SKILL)
        dmg_.add_bonus_enum(bonus, DmgTypes.BURST)
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return alhaitham_a4


def tighnari_c1(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    crit_rate += 0.15
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def tighnari_c2(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus_enum(0.2, GenshinData.ElementTypes.DENDRO)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def tighnari_a4_builder(tighnari):
    def tighnari_a4(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        bonus = min(tighnari.em * 0.0006, 0.6)
        dmg_.add_bonus_enum(bonus, DmgTypes.CHARGE)
        dmg_.add_bonus_enum(bonus, DmgTypes.BURST)
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return tighnari_a4


def tighnari_a1(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 50
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


# Artifacts
def thundering_fury_2p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus_enum(0.15, GenshinData.ElementTypes.ELECTRO)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em

# TODO expensive
def thundering_fury_4p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    reaction_bonus.add_bonus(0.40, Reactions.OVERLOAD)
    reaction_bonus.add_bonus(0.40, Reactions.CHARGE)
    reaction_bonus.add_bonus(0.40, Reactions.SCOND)
    reaction_bonus.add_bonus(0.40, Reactions.HBLOOM)
    reaction_bonus.add_bonus(0.20, Reactions.AGG)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def vv_4p_builder(element):
    def vv_4p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        def_redu.add_bonus(0.4, element)
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return vv_4p


def wandererstroupe_2p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 80
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def wandererstroupe_4p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus_enum(0.35, DmgTypes.CHARGE)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def deepwood_2p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus_enum(0.35, GenshinData.ElementTypes.DENDRO)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def deepwood_4p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    def_redu.add_bonus_enum(0.30, GenshinData.ElementTypes.DENDRO)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def gildeddreams_2p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    em += 80
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em

def gildeddreams_4p_builder(same, diff):
    def gilded_dreams_4p(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        atk_ += 0.14 * min(same, 3)
        em += 50 * min(diff, 3)
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return gilded_dreams_4p


artifact_buff_quick_add = {
    'ThunderingFury2': thundering_fury_2p,
    'ThunderingFury4': thundering_fury_4p,
    'WanderersTroupe2': wandererstroupe_2p,
    'WanderersTroupe4': wandererstroupe_4p,
    'DeepwoodMemories2': deepwood_2p,
    'DeepwoodMemories4': deepwood_4p,
    'GildedDreams2': gildeddreams_2p,
    'GildedDreams4': None  # requires extra data. Need to replace in the optimizer function
}


# Weapons
def mistsplitter_builder(stacks): # TODO expensive
    def mistsplitter_buff(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        amounts = [0.08, 0.16, 0.28]
        total_boost = 0.12 + amounts[stacks]
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.ELECTRO)
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.PYRO)
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.CRYO)
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.HYDRO)
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.ANEMO)
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.GEO)
        dmg_.add_bonus_enum(total_boost, GenshinData.ElementTypes.DENDRO)
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return mistsplitter_buff


def thousand_dreams_builder(same):
    def thousand_dreams(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        if same:
            em += 32
        else:
            # TODO DMG bonus for only the characters type (this is close enough for now
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.ELECTRO)
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.PYRO)
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.CRYO)
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.HYDRO)
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.ANEMO)
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.GEO)
            dmg_.add_bonus_enum(0.10, GenshinData.ElementTypes.DENDRO)
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return thousand_dreams


def foliar_incision_builder(char):
    def foliar_incision(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        crit_rate += 0.04
        flat_dmg += char.em * 1.2
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return foliar_incision


def stringless(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus_enum(0.48, DmgTypes.SKILL)
    dmg_.add_bonus_enum(0.48, DmgTypes.BURST)
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em

#Resonance
def pyro_res(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    atk_ += 0.25
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def cryo_res(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    crit_rate += 0.15
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def geo_res(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
    dmg_.add_bonus(0.15, GenshinData.ElementTypes.ALL)
    def_redu += 0.2
    return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def dendro_res_builder(after_primary, after_secondary):
    em_bonus = 50
    if after_primary:
        em_bonus += 30
    if after_secondary:
        em_bonus += 20

    def dendro_res(talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, dmg_, em, reaction, reaction_bonus, def_redu):
        em += em_bonus
        return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em
    return dendro_res
