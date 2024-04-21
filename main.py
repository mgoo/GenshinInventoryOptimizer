import json
import math
import copy

import pandas as pd
from pandas import ExcelWriter
from tqdm import tqdm
import multiprocessing

import buffs
from characters import Account, character_cache
from optimizer import Optimizer
from utils import load_json_data

from genshin_data import GenshinData


def all_possibilities(artifact, rolls_left):
    """
    Finds all possible options when leveling an artifact to 20
    # TODO weight based on new substat!!
    :param artifact:
    :param rolls_left:
    :return:
    """
    # Exit Condition
    if rolls_left == 0:
        return [artifact]

    #Operation
    possibilities = []
    if len(artifact['sub_stats']) != 4:
        # Add Substat
        # TODO handle weighting properly!!
        for sub_stat in GenshinData.possible_sub_stats.keys():
            if sub_stat in artifact['sub_stats']:
                continue
            # for rv in sub_stat_rolls:
            #     possibility = copy.deepcopy(artifact)
            #     possibility['sub_stats'][sub_stat] = possible_sub_stats[sub_stat]['max_roll'] * rv
            #     possibilities.append(possibility)
            possibility = copy.deepcopy(artifact)
            possibility['sub_stats'][sub_stat] = GenshinData.possible_sub_stats[sub_stat]['max_roll'] * .85
            possibilities.append(possibility)
    else:
        # Add roll
        for sub_stat in artifact['sub_stats']:
            # for rv in sub_stat_rolls:
            #     possibility = copy.deepcopy(artifact)
            #     possibility['sub_stats'][sub_stat] += possible_sub_stats[sub_stat]['max_roll'] * rv
            #     possibilities.append(possibility)
            possibility = copy.deepcopy(artifact)
            possibility['sub_stats'][sub_stat] += GenshinData.possible_sub_stats[sub_stat]['max_roll'] * .85
            possibilities.append(possibility)
    # Recursion
    res = []
    for possibility in possibilities:
        for final_pos in all_possibilities(possibility, rolls_left - 1):
            res.append(final_pos)
    return res


if __name__ == '__main__':
    # pool = multiprocessing.Pool(8)

    account = Account("resources/account_data/genshinData_GOOD_2024_04_20_18_33.json")

    char_data = GenshinData.load_char_data("resources/genshin_data/genshin_char_data_4_1.csv")

    character_name = 'KukiShinobu'
    # set = 'GildedDreams'
    # set = 'WanderersTroupe'
    set = 'ThunderingFury'
    element = 'electro_'

    character = account.characters[character_name]

    # Cache party to speed up calcs
    sucrose = account.characters['Sucrose']
    sucrose.apply_buffs([buffs.collei_c4])
    character_cache['Sucrose'] = sucrose

    results = {}
    for slot_to_optimize in ['flower', 'plume', 'sands', 'circlet', 'goblet']:
        print('***' + slot_to_optimize + '***')

        if slot_to_optimize == 'goblet':
            tf_artifacts = account.artifacts[(account.artifacts['main_stat'] == element) & (account.artifacts['slot'] == slot_to_optimize)].to_dict('records')
        else:
            tf_artifacts = account.artifacts[(account.artifacts['set'] == set) & (account.artifacts['slot'] == slot_to_optimize)].to_dict('records')
            # tf_artifacts = artifacts_df[(artifacts_df['slot'] == slot_to_optimize)].to_dict('records')

        calced_artifacts = []
        for idx, artifact in enumerate(tf_artifacts):
            rolls_left = 5 - math.floor(artifact['level'] / 4)
            # convert artifact to find all possibilities
            artifact['main_stat_value'] = GenshinData.possible_main_stats[artifact['main_stat']]['max_value']
            artifact['sub_stats'] = {}
            for sub_stat in GenshinData.possible_sub_stats.keys():
                if artifact[sub_stat] != 0:
                    artifact['sub_stats'][sub_stat] = artifact[sub_stat]
                artifact.pop(sub_stat)

            # Find all possible options when leveling up the artifact
            options = all_possibilities(copy.deepcopy(artifact), rolls_left)

            values = [
                Optimizer().get_value(option, character, account)
                for option in tqdm(options, desc='calculating: {idx}/{total}'.format(idx=idx + 1, total=len(tf_artifacts)))
            ]

            artifact['avg_value'] = sum(values) / len(values)
            calced_artifacts.append(artifact)
        results[slot_to_optimize] = pd.DataFrame(calced_artifacts)
    with ExcelWriter('output/{char}_{set}.xlsx'.format(char=character.name, set=set)) as writer:
        for slot, df in results.items():
            df.sort_values('avg_value').to_excel(writer, slot)
        pd.concat([frame for frame in results.values()], axis=0).sort_values('avg_value').to_excel(writer, 'Combine')
    print("Done")


