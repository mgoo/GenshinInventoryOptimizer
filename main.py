import json
import math
import copy

import pandas as pd
from pandas import ExcelWriter
from tqdm import tqdm
import multiprocessing

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
    pool = multiprocessing.Pool(8)

    account_data = load_json_data("resources/account_data/genshinData_GOOD_2024_04_20_18_33.json")

    artifacts = account_data["artifacts"]
    artifacts_df = GenshinData.tabulate_artifacts(artifacts)

    char_data = GenshinData.load_char_data("resources/genshin_data/genshin_char_data_4_1.csv")

    character = 'KukiShinobu'
    set = 'ThunderingFury'

    char_artifact_list = artifacts_df.loc[artifacts_df["location"] == character].to_dict('records')
    char_artifacts = dict()
    for artifact in char_artifact_list:
        artifact['sub_stats'] = dict()
        for sub_stat in GenshinData.possible_sub_stats.keys():
            if artifact[sub_stat] != 0:
                artifact['sub_stats'][sub_stat] = artifact[sub_stat]
            artifact.pop(sub_stat)
        char_artifacts[artifact['slot']] = artifact

    results = {}
    for slot_to_optimize in ['flower', 'plume', 'sands', 'circlet', 'goblet']:
        print('***' + slot_to_optimize + '***')

        fixed_artifacts = dict()
        for key, item in char_artifacts.items():
            if key != slot_to_optimize:
                fixed_artifacts[key] = item

        if slot_to_optimize == 'goblet':
            tf_artifacts = artifacts_df[(artifacts_df['main_stat'] == 'electro_') & (artifacts_df['slot'] == slot_to_optimize)].to_dict('records')
        else:
            tf_artifacts = artifacts_df[(artifacts_df['set'] == set) & (artifacts_df['slot'] == slot_to_optimize)].to_dict('records')

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


            args = [{
                'option': option,
                'possible_sub_stats': GenshinData.possible_sub_stats,
                'fixed_artifacts': fixed_artifacts.copy(),
                'weapon': GenshinData.weapons['homa'],
                'char_data': char_data.loc['Keqing'] # TODO unify Char names
            } for option in options]
            # values = list(tqdm(
            #     pool.imap(Optimizer().get_value, args),
            #     total=len(args),
            #     desc='calculating: {idx}/{total}'.format(idx=idx + 1, total=len(tf_artifacts))
            # ))
            values = [Optimizer().get_value(arg) for arg in tqdm(args, desc='calculating: {idx}/{total}'.format(idx=idx + 1, total=len(tf_artifacts)))]

            artifact['avg_value'] = sum(values) / len(values)
            calced_artifacts.append(artifact)
        results[slot_to_optimize] = pd.DataFrame(calced_artifacts)
    with ExcelWriter('output/{char}_{set}.xlsx'.format(char=character, set=set)) as writer:
        for slot, df in results.items():
            df.to_excel(writer, slot)
        pd.concat([frame for frame in results.values()], axis=0).to_excel(writer, 'Combine')
    print("Done")


