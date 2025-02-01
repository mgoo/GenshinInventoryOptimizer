import json
import math
import copy

import pandas as pd
from pandas import ExcelWriter
from tqdm import tqdm
import multiprocessing

from buffs import *
from characters import Account, character_cache
from optimizer import Optimizer
from utils import load_json_data

from genshin_data import GenshinData


def all_possibilities(artifacts):
    """
    Finds all possible options when leveling an artifact to 20
    # TODO weight based on new substat!!
    :param artifact:
    :param rolls_left:
    :return:
    """
    # Exit Condition
    if all([0 == 5 - math.floor(artifact['level'] / 4) for artifact in artifacts.values()]):
        return [artifacts]

    res = []
    for slot, artifact in artifacts.items():

        rolls_left = 5 - math.floor(artifact['level'] / 4)
        if rolls_left == 0:
            continue

        #Operation
        possibilities = []
        if len(artifact['sub_stats']) != 4:
            # Add Substat
            # TODO handle weighting properly!!
            for sub_stat in GenshinData.possible_sub_stats.keys():
                if sub_stat in artifact['sub_stats']:
                    continue
                possibility = dict(artifact)
                possibility['sub_stats'] = dict(artifact['sub_stats'])
                GenshinData.max_artifact_id += 1
                possibility['id'] = GenshinData.max_artifact_id

                possibility['sub_stats'][sub_stat] = GenshinData.possible_sub_stats[sub_stat]['max_roll'] * .85
                possibilities.append(possibility)
        else:
            # Add roll
            for sub_stat in artifact['sub_stats']:
                possibility = dict(artifact)
                possibility['sub_stats'] = dict(artifact['sub_stats'])
                GenshinData.max_artifact_id += 1
                possibility['id'] = GenshinData.max_artifact_id

                possibility['sub_stats'][sub_stat] += GenshinData.possible_sub_stats[sub_stat]['max_roll'] * .85
                possibilities.append(possibility)
        # Recursion
        for possibility in possibilities:
            possibility['level'] = min(possibility['level'] + 4, 20)
            possible_set = copy.copy(artifacts)
            possible_set[slot] = possibility
            for final_pos in all_possibilities(possible_set):
                res.append(final_pos)
    return res


if __name__ == '__main__':
    pool = multiprocessing.Pool(8)

    account = Account("resources/account_data/genshinData_GOOD_2024_04_22_20_23.json")

    char_data = GenshinData.load_char_data("resources/genshin_data/genshin_char_data_4_1.csv")

    character_name = 'KukiShinobu'
    # set = 'GildedDreams'
    # set = 'WanderersTroupe'
    set = 'ThunderingFury'
    element = 'electro_'

    character = account.characters[character_name]

    sucrose = account.characters['Sucrose']
    sucrose.apply_buffs([collei_c4])

    character.apply_buffs([
        vv_4p_builder(GenshinData.ElementTypes.ELECTRO), sucrose_a1, sucrose_a4_builder(sucrose),
        collei_c4,
        mistsplitter_builder(2)
    ])

    initial_artifacts = copy.deepcopy(character.artifacts)

    results = {}
    for slot_to_optimize in ['flower', 'plume', 'sands', 'goblet', 'circlet']:
        print('***' + slot_to_optimize + '***')

        if slot_to_optimize == 'goblet':
            tf_artifacts = account.artifacts[(account.artifacts['main_stat'] == element) & (account.artifacts['slot'] == slot_to_optimize) & (account.artifacts['rarity'] == 5)].to_dict('records')
        else:
            tf_artifacts = account.artifacts[(account.artifacts['set'] == set) & (account.artifacts['slot'] == slot_to_optimize) & (account.artifacts['rarity'] == 5)].to_dict('records')
            # tf_artifacts = artifacts_df[(artifacts_df['slot'] == slot_to_optimize)].to_dict('records')

        calced_artifacts = []
        for idx, artifact in enumerate(tf_artifacts):

            # convert artifact to find all possibilities
            artifact['main_stat_value'] = GenshinData.possible_main_stats[artifact['main_stat']]['max_value']
            artifact = GenshinData.dictionise_row(artifact)
            artifact[artifact['slot']] = artifact

            # Find all possible options when leveling up the artifact
            artifacts = copy.deepcopy(initial_artifacts)
            artifacts[slot_to_optimize] = artifact
            options = all_possibilities(artifacts)

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


