import autograd.numpy as np

from genshin_data import GenshinData

class StatBlock:
    def __init__(self, values: dict):
        self._stats = {stat: 0 for stat in GenshinData.stat_names}
        for stat in GenshinData.stat_names:
            if stat in values:
                self._stats[stat] = values[stat]

    def __getitem__(self, item):
        return self._stats[item]

    def total_atk(self):
        return (self._stats['base_atk'] * (1 + self._stats['atk_'])) + self._stats['atk']

    def total_def(self):
        return (self._stats['base_def'] * (1 + self._stats['def_'])) + self._stats['def']

    def total_hp(self):
        return (self._stats['base_hp'] * (1 + self._stats['hp_'])) + self._stats['hp']

    def get_non_zero(self):
        return {key:value for key, value in self._stats.items() if value != 0}

    def add(self, stat, value):
        new_block = StatBlock({stat: value})
        return self + new_block

    def __add__(self, other):
        return StatBlock({key: self._stats[key] + other._stats[key] for key in self._stats.keys()})

    def __sub__(self, other):
        return StatBlock({key: self._stats[key] - other._stats[key] for key in self._stats.keys()})

    def __copy__(self):
        return StatBlock(self._stats.copy())

    def as_array(self):
        return np.array([self[stat_name] for stat_name in GenshinData.stat_names])

