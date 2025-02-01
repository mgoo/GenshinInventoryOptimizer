from enum import Enum

# Assume Lv 90
from stat_block import StatBlock

_agg_base = 1663.88
_spread_base = 1808.57
_swirl_base = 868.1
_trans_base = 1446.85


def dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu):
    enemy_def_mult = (100 + 100) / ( (100 + 100) + ((100 + 100) * (1 - def_redu)) )
    return base_dmg * avg_crit_bonus * dmg_ * enemy_def_mult


def _forward_amplify(em, bonus):
    return 2 * (1 + (2.78*em) / (1400 + em) + bonus)


def _back_amplify(em, bonus):
    return 1.5 * (1 + (2.78 * em) / (1400 + em) + bonus)


def _transformative(em, bonus, multiplier):
    return multiplier * _trans_base * (1 + (16 * em) / (2000 + em) + bonus)


class Reactions(Enum):
    NONE = '0'
    F_VAPE = '1'
    B_VAPE = '2'
    F_MELT = '3'
    B_MELT = '4'
    SPREAD = '5'
    AGG = '6'
    SWIRL = '7'
    HBLOOM = '8'
    BURGEON = '9'
    OVERLOAD = '10'
    BLOOM = '11'
    SHATTER = '12'
    CHARGE = '13'
    SCOND = '14'
    BURNING = '15'

    def calc_dmg(
            self,
            talent_, char_stats: StatBlock,
            atk_type, element
    ):
        total_atk = char_stats.total_atk()
        total_hp = char_stats.total_hp()
        total_def = char_stats.total_def()
        flat_dmg = char_stats['dmg']
        crit_rate = char_stats['crit_rate']
        crit_dmg = char_stats['crit_dmg']

        dmg_ = char_stats['dmg_'] + char_stats[element.value] + char_stats[atk_type.value + '_']
        em = char_stats['em']

        def_redu = char_stats['def_redu_']

        avg_crit_bonus = 1 + min(max(0, crit_rate), 1) * crit_dmg
        base_dmg = sum([talent_mult(char_stats) for talent_mult in talent_]) + flat_dmg

        if self == Reactions.NONE:
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu)
        if self == Reactions.F_VAPE:
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu) * _forward_amplify(em, char_stats['vape_'])
        elif self == Reactions.B_VAPE:
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu) * _back_amplify(em, char_stats['vape_'])
        elif self == Reactions.F_MELT:
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu) * _forward_amplify(em, char_stats['melt_'])
        elif self == Reactions.B_MELT:
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu) * _back_amplify(em, char_stats['melt_'])
        elif self == Reactions.SPREAD:
            base_dmg += 1.25 * _spread_base * (1 + (5*em)/(1200+em) + char_stats['spread_'])
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu)
        elif self == Reactions.AGG:
            base_dmg += 1.15 * _agg_base * (1 + (5*em)/(1200+em) + char_stats['agg_'])
            return dmg_formula(base_dmg, avg_crit_bonus, dmg_, element, def_redu)
        elif self == Reactions.HBLOOM or self == Reactions.BURGEON:
            return _transformative(em, char_stats['hbloom_'], 3)
        elif self == Reactions.OVERLOAD or self == Reactions.BLOOM:
            return _transformative(em, char_stats['over_'], 2)
        elif self == Reactions.SHATTER:
            return _transformative(em, char_stats['shatter_'], 1.5)
        elif self == Reactions.CHARGE:
            return _transformative(em, char_stats['echarg_'], 1.2)
        elif self == Reactions.SWIRL:
            return _transformative(em, char_stats['swirl_'], 0.6)
        elif self == Reactions.SCOND:
            return _transformative(em, char_stats['scond_'], 0.5)
        elif self == Reactions.BURNING:
            return _transformative(em, char_stats['burn_'], 0.25)
        else:
            raise Exception('Reaction not found')


class ReactionBonuses:
    def __init__(self):
        self._react = dict()
        for key in Reactions:
            self._react[key.value] = 0

    def get(self, type):
        if isinstance(type, Reactions):
            type = type.value
        return self._react[type]

    def add_bonus(self, amount, type):
        if isinstance(type, Reactions):
            type = type.value
        self._react[type] += amount