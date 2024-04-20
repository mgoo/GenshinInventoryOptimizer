from enum import Enum

# Assume Lv 90
_agg_base = 1663.88
_spread_base = 1808.57
_swirl_base = 868.1


def dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu):
    enemy_def_mult = (100 + 100) / ( (100 + 100) + ((100 + 100) * (1 - def_redu.get(element))) )
    return talent_ * total_atk * avg_crit_bonus * dmg_.get(element, atk_type) * enemy_def_mult


def _forward_amplify(em, bonus):
    return 2 * (1 + (2.78*em) / (1400 + em) + bonus)


def _back_amplify(em, bonus):
    return 1.5 * (1 + (2.78 * em) / (1400 + em) + bonus)


class Reactions(Enum):
    NONE = '0'
    F_VAPE = '1'
    B_VAPE = '2'
    F_MELT = '3'
    B_MELT = '4'
    SPREAD = '5'
    AGG = '6'
    SWIRL = '7'

    def calc_dmg(self, talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_, em, atk_type, element, bonus, def_redu):
        total_atk = base_atk * (1 + atk_) + flat_atk
        avg_crit_bonus = 1 + max(0, crit_rate) * crit_dmg

        if self == Reactions.NONE:
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu)
        if self == Reactions.F_VAPE:
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu) * _forward_amplify(em, bonus.get(ReactionTypes.VAPE))
        elif self == Reactions.B_VAPE:
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu) * _back_amplify(em, bonus.get(ReactionTypes.VAPE))
        elif self == Reactions.F_MELT:
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu) * _forward_amplify(em, bonus.get(ReactionTypes.MELT))
        elif self == Reactions.B_MELT:
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu) * _back_amplify(em, bonus.get(ReactionTypes.MELT))
        elif self == Reactions.SPREAD:
            total_atk += 1.25 * _spread_base * (1 + (5*em)/(1200+em) + bonus.get(ReactionTypes.SPREAD))
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu)
        elif self == Reactions.AGG:
            total_atk += 1.15 * _agg_base * (1 + (5*em)/(1200+em) + bonus.get(ReactionTypes.AGG))
            return dmg_formula(talent_, total_atk, avg_crit_bonus, dmg_, atk_type, element, def_redu)
        elif self == Reactions.SWIRL:
            # TODO idk if this is right
            return talent_ * total_atk * avg_crit_bonus * dmg_ + 0.6 * _swirl_base * (1 + (16 * em)/(2000+em) + bonus[ReactionTypes.SWIRL])
        else:
            raise Exception('Reaction not found')


class ReactionTypes(Enum):
    NONE = '0'
    VAPE = '1'
    MELT = '2'
    SPREAD = '3'
    AGG = '4'
    SWIRL = '5'
    BURN = '6'
    BLOOM = '7'
    HBLOOM = '8'
    SCOND = '9'
    CHARGE = 'a'
    OVERLOAD = 'b'


class ReactionBonuses:
    def __init__(self):
        self._react = dict()
        for key in ReactionTypes:
            self._react[key.value] = 0

    def get(self, type):
        if isinstance(type, ReactionTypes):
            type = type.value
        return self._react[type]

    def add_bonus(self, amount, type):
        if isinstance(type, ReactionTypes):
            type = type.value
        self._react[type] += amount