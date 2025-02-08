from enum import Enum

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

    @staticmethod
    def forward_amplify(em, bonus):
        return 2 * (1 + (2.78 * em) / (1400 + em) + bonus)

    @staticmethod
    def back_amplify(em, bonus):
        return 1.5 * (1 + (2.78 * em) / (1400 + em) + bonus)

    @staticmethod
    def transformative(em, bonus, multiplier):
        return multiplier * Reactions.trans_base() * (1 + (16 * em) / (2000 + em) + bonus)

    @staticmethod
    def spread(em, spread_):
        return 1.25 * Reactions.spread_base() * (1 + (5 * em) / (1200 + em) + spread_)

    @staticmethod
    def agg(em, agg_):
        return 1.15 * Reactions.agg_base() * (1 + (5*em)/(1200+em) + agg_)

    @staticmethod
    def agg_base(lv=90):
        # TODO implement level scaling
        return 1663.88

    @staticmethod
    def spread_base(lv=90):
        # TODO implement level scaling
        return 1808.57

    @staticmethod
    def swirl_base(lv=90):
        # TODO implement level scaling I Dont think I need this. I should check the reaction stuff
        return 868.1

    @staticmethod
    def trans_base(lv=90):
        # TODO implement level scaling
        return 1446.85


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