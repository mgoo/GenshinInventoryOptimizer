from collections import defaultdict

import torch
from torch.nn.functional import softmax

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from characters import Account
from genshin_data import GenshinData
from stat_block import StatBlock

from optimization_targets import KeqingAgg


class OptimizerStatBlock(StatBlock):
    parameter_names = GenshinData.stat_names

    @classmethod
    def from_stat_block(cls, stat_block: StatBlock):
        return cls(stat_block._stats)

    def to_stat_block(self):
        return StatBlock({key: self[key] for key in self.parameter_names})

    def __init__(self, values: dict):
        super().__init__(values)
        self._stats = torch.tensor([values[stat] if stat in values else 0 for stat in self.parameter_names], dtype=torch.float64)

    def get_idx(self, stat):
        return self.parameter_names.index(stat)

    def __getitem__(self, item):
        return self._stats[self.get_idx(item)]

    def total_atk(self):
        return (self._stats[self.get_idx('base_atk')] * (1 + self._stats[self.get_idx('atk_')])) + self._stats[self.get_idx('atk')]

    def total_def(self):
        return (self._stats[self.get_idx('base_def')] * (1 + self._stats[self.get_idx('def_')])) + self._stats[self.get_idx('def')]

    def total_hp(self):
        return (self._stats[self.get_idx('base_hp')] * (1 + self._stats[self.get_idx('hp_')])) + self._stats[self.get_idx('hp')]

    def get_non_zero(self):
        raise Exception('not yet implemented')

    def add(self, stat, value):
        new_block = OptimizerStatBlock({stat: value})
        return self + new_block

    def __add__(self, other):
        if isinstance(other, OptimizerStatBlock):
            new_block = OptimizerStatBlock({})
            new_block._stats = self._stats + other._stats
            return new_block
        elif isinstance(other, StatBlock):
            opt_other = OptimizerStatBlock.from_stat_block(other)
            return self + opt_other
        raise Exception('not accepted type')

    def __sub__(self, other):
        new_block = OptimizerStatBlock({})
        new_block._stats = self._stats - other._stats
        return new_block

    def __copy__(self):
        new_block = OptimizerStatBlock({})
        new_block._stats = self._stats.copy()
        return new_block

    def as_array(self):
        return self._stats


def artifact_filter_4p(account, set, offset_slot):
    results = []
    for artifact in account.artifacts.values():
        if artifact.set_key == set or artifact.slot_key == offset_slot:
            results.append(artifact)
    return results

def optimize(target, account, character, arti_set, offset_slot, verbose=False):
    weapons = [wep for wep in account.weapons.values()]

    char_stats = torch.tensor(OptimizerStatBlock.from_stat_block(character.stat_block).as_array(), dtype=torch.float64)

    artifact_options = artifact_filter_4p(account, arti_set, offset_slot)
    artifacts = defaultdict(lambda: list())
    for artifact in artifact_options:
        artifacts[artifact.slot_key].append(artifact)

    flower_stats = torch.stack([OptimizerStatBlock.from_stat_block(arti.total_stat_boost()).as_array() for arti in artifacts['flower']])
    plume_stats = torch.stack([OptimizerStatBlock.from_stat_block(arti.total_stat_boost()).as_array() for arti in artifacts['plume']])
    sands_stats = torch.stack([OptimizerStatBlock.from_stat_block(arti.total_stat_boost()).as_array() for arti in artifacts['sands']])
    goblet_stats = torch.stack([OptimizerStatBlock.from_stat_block(arti.total_stat_boost()).as_array() for arti in artifacts['goblet']])
    circlet_stats = torch.stack([OptimizerStatBlock.from_stat_block(arti.total_stat_boost()).as_array() for arti in artifacts['circlet']])

    # Fixed Initialization
    # flower_weights = torch.tensor([1 for _ in range(flower_stats.shape[0])], dtype=torch.float64, requires_grad=True)
    # plume_weights = torch.tensor([1 for _ in range(plume_stats.shape[0])], dtype=torch.float64, requires_grad=True)
    # sands_weights = torch.tensor([1 for _ in range(sands_stats.shape[0])], dtype=torch.float64, requires_grad=True)
    # goblet_weights = torch.tensor([1 for _ in range(goblet_stats.shape[0])], dtype=torch.float64, requires_grad=True)
    # circlet_weights = torch.tensor([1 for _ in range(circlet_stats.shape[0])], dtype=torch.float64, requires_grad=True)

    # Random Initialization
    flower_weights = torch.rand(flower_stats.shape[0], requires_grad=True)
    plume_weights = torch.rand(plume_stats.shape[0], requires_grad=True)
    sands_weights = torch.rand(sands_stats.shape[0], requires_grad=True)
    goblet_weights = torch.rand(goblet_stats.shape[0], requires_grad=True)
    circlet_weights = torch.rand(circlet_stats.shape[0], requires_grad=True)

    possible_weapons = [wep for wep in weapons if wep.weapon_class == character.weapon_class]
    weapons_stats = torch.stack([OptimizerStatBlock.from_stat_block(wep.stat_block + wep.get_buffs()).as_array() for wep in possible_weapons])
    weapon_weights = torch.tensor([1 for _ in range(weapons_stats.shape[0])], dtype=torch.float64, requires_grad=True)

    def forward(weapon_weights, flower_weights, plume_weights, sands_weights, goblet_weights, circlet_weights):
        final_weapon_stats = torch.sum(torch.mul(softmax(weapon_weights, dim=0)[:, None], weapons_stats), dim=0)

        final_flower_stats = torch.sum(torch.mul(softmax(flower_weights, dim=0)[:, None], flower_stats), dim=0)
        final_plume_stats = torch.sum(torch.mul(softmax(plume_weights, dim=0)[:, None], plume_stats), dim=0)
        final_sands_stats = torch.sum(torch.mul(softmax(sands_weights, dim=0)[:, None], sands_stats), dim=0)
        final_goblet_stats = torch.sum(torch.mul(softmax(goblet_weights, dim=0)[:, None], goblet_stats), dim=0)
        final_circlet_stats = torch.sum(torch.mul(softmax(circlet_weights, dim=0)[:, None], circlet_stats), dim=0)

        stats = char_stats + final_flower_stats + final_plume_stats + final_sands_stats + final_goblet_stats + final_circlet_stats + final_weapon_stats

        block = OptimizerStatBlock({})
        block._stats = stats

        return target.target_function(block, account)

    lr = 0.1
    epochs = 20

    dmg_hist = []
    weapon_weights_hist = []
    flower_weights_hist = []
    plume_weights_hist = []
    sands_weights_hist = []
    goblet_weights_hist = []
    circlet_weights_hist = []
    weapon_weights_grad_hist = []
    flower_weights_grad_hist = []
    plume_weights_grad_hist = []
    sands_weights_grad_hist = []
    goblet_weights_grad_hist = []
    circlet_weights_grad_hist = []

    weapon_weights_hist.append(weapon_weights.detach().numpy())
    flower_weights_hist.append(flower_weights.detach().numpy())
    plume_weights_hist.append(plume_weights.detach().numpy())
    sands_weights_hist.append(sands_weights.detach().numpy())
    goblet_weights_hist.append(goblet_weights.detach().numpy())
    circlet_weights_hist.append(circlet_weights.detach().numpy())

    for epoch in range(epochs):
        dmg_value = forward(weapon_weights, flower_weights, plume_weights, sands_weights, goblet_weights, circlet_weights)
        dmg_value.backward()

        if verbose:
            print('*********** Epoch:', epoch, '***********')
            print('Total dmg:', dmg_value.item())
            print('weapon:', torch.mean(weapon_weights.grad))
            print('flower:', torch.mean(flower_weights.grad))
            print('plume:', torch.mean(plume_weights.grad))
            print('sands:', torch.mean(sands_weights.grad))
            print('goblet:', torch.mean(goblet_weights.grad))
            print('circlet:', torch.mean(circlet_weights.grad))

        dmg_hist.append(dmg_value.item())
        weapon_weights_grad_hist.append(weapon_weights.grad.numpy())
        flower_weights_grad_hist.append(flower_weights.grad.numpy())
        plume_weights_grad_hist.append(plume_weights.grad.numpy())
        sands_weights_grad_hist.append(sands_weights.grad.numpy())
        goblet_weights_grad_hist.append(goblet_weights.grad.numpy())
        circlet_weights_grad_hist.append(circlet_weights.grad.numpy())

        weapon_weights = torch.tensor(weapon_weights + weapon_weights.grad * lr, requires_grad=True)
        flower_weights = torch.tensor(flower_weights + flower_weights.grad * lr, requires_grad=True)
        plume_weights = torch.tensor(plume_weights + plume_weights.grad * lr, requires_grad=True)
        sands_weights = torch.tensor(sands_weights + sands_weights.grad * lr, requires_grad=True)
        goblet_weights = torch.tensor(goblet_weights + goblet_weights.grad * lr, requires_grad=True)
        circlet_weights = torch.tensor(circlet_weights + circlet_weights.grad * lr, requires_grad=True)

        weapon_weights_hist.append(weapon_weights.detach().numpy())
        flower_weights_hist.append(flower_weights.detach().numpy())
        plume_weights_hist.append(plume_weights.detach().numpy())
        sands_weights_hist.append(sands_weights.detach().numpy())
        goblet_weights_hist.append(goblet_weights.detach().numpy())
        circlet_weights_hist.append(circlet_weights.detach().numpy())

    if verbose:
        best_weapon = torch.argmax(weapon_weights)
        print(possible_weapons[best_weapon].name)

        best_flower = artifacts['flower'][torch.argmax(flower_weights)]
        best_plume = artifacts['plume'][torch.argmax(plume_weights)]
        best_sands = artifacts['sands'][torch.argmax(sands_weights)]
        best_goblet = artifacts['goblet'][torch.argmax(goblet_weights)]
        best_circlet = artifacts['circlet'][torch.argmax(circlet_weights)]

        print('flower:', best_flower.sub_stats)
        print('plume:', best_plume.sub_stats)
        print('sands:', best_sands.main_stat, best_sands.sub_stats)
        print('goblet:', best_goblet.main_stat, best_goblet.sub_stats)
        print('circlet:', best_circlet.main_stat, best_circlet.sub_stats)

        dmg_hist_df = pd.DataFrame({
            'dmg_hist': dmg_hist,
            'epoch': range(len(dmg_hist))
        })
        fig = px.line(dmg_hist_df, x='epoch', y='dmg_hist', title='Damage History')
        fig.show()

        fig = go.Figure()
        for epoch, weights in enumerate(goblet_weights_grad_hist):
            shade = 150 - (100 * epoch / len(goblet_weights_grad_hist))
            fig.add_trace(go.Scatter(x=list(range(weights.shape[0])), y=weights, line={'color': 'rgb({r}, {g}, {b})'.format(r=shade, g=shade, b=shade)}))
        fig.show()

    ordered_weapons = sorted(zip(possible_weapons, weapon_weights.tolist()), key=lambda pair: pair[1], reverse=True)
    ordered_flowers = sorted(zip(artifacts['flower'], flower_weights.tolist()), key=lambda pair: pair[1], reverse=True)
    ordered_plumes = sorted(zip(artifacts['plume'], plume_weights.tolist()), key=lambda pair: pair[1], reverse=True)
    ordered_sands = sorted(zip(artifacts['sands'], sands_weights.tolist()), key=lambda pair: pair[1], reverse=True)
    ordered_goblets = sorted(zip(artifacts['goblet'], goblet_weights.tolist()), key=lambda pair: pair[1], reverse=True)
    ordered_circlets = sorted(zip(artifacts['circlet'], circlet_weights.tolist()), key=lambda pair: pair[1], reverse=True)

    return (
        ordered_weapons,
        ordered_flowers,
        ordered_plumes,
        ordered_sands,
        ordered_goblets,
        ordered_circlets,

        dmg_hist,

        weapon_weights_hist,
        flower_weights_hist,
        plume_weights_hist,
        sands_weights_hist,
        goblet_weights_hist,
        circlet_weights_hist,

        weapon_weights_grad_hist,
        flower_weights_grad_hist,
        plume_weights_grad_hist,
        sands_weights_grad_hist,
        goblet_weights_grad_hist,
        circlet_weights_grad_hist
    )

# if __name__ == '__main__':
#     optimize()