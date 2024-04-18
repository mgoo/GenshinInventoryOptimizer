from reactions import Reactions


# Characters
def bennett_builder(wep_atk):
    def bennett_buff(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
        ratio = 1.12 + .20
        bennett_base_atk = 191.16
        flat_atk += (ratio * (bennett_base_atk + wep_atk))
        return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu
    return bennett_buff


def sucrose_a1(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
    em += 50
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu


def sucrose_a4(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
    em += 169.73  # 20% of sucrose em
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu


def collei_c4(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
    em += 60
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu


# Artifacts
def thundering_fury_2p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
    dmg_bonus_ += 0.15
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu


def thundering_fury_4p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
    if reaction == Reactions.AGG:
        reaction_bonus += .20
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu


def vv_4p(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
    def_redu += 0.4
    return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu


# Weapons
def mistsplitter_builder(stacks):
    def mistsplitter_buff(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu):
        amounts = [0.08, 0.16, 0.28]
        total_boost = 0.12 + amounts[stacks]
        dmg_bonus_ += total_boost
        return talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu
    return mistsplitter_buff