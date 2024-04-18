import json
import math
import copy

import pandas as pd
from pandas import ExcelWriter
from tqdm import tqdm
import multiprocessing

from buffs import *
from reactions import Reactions


avg_artifact_num = 1.065
three_line_percent_domain = .8
three_line_percent_strong_box = .66

char_base_crit_rate = .05
char_base_crit_dmg = .5

stat_name_mapping = {
    "hp": "hp", "HP": "hp",
    "hp_": "hp_", "HP%": "hp_",
    "atk": "atk", "ATK": "atk",
    "atk_": "atk_", "ATK%": "atk_",
    "def": "def", "DEF": "def",
    "def_": "def_", "DEF%": "def_",
    "crit_dmg": "crit_dmg", "Crit DMG%": "crit_dmg", "critDMG_": "crit_dmg",
    "crit_rate": "crit_rate", "Crit Rate%": "crit_rate", "critRate_": "crit_rate",
    "em": "em", "Elemental Mastery": "em", "eleMas": "em",
    "er_": "er_", "Energy Recharge%": "er_", "enerRech_": "er_",

    "pyro_": "pyro_", "pyro_dmg_": "pyro_",
    "electro_": "electro_", "electro_dmg_": "electro_",
    "cryo_": "cryo_", "cryo_dmg_": "cryo_",
    "hydro_": "hydro_", "hydro_dmg_": "hydro_",
    "dendro_": "dendro_", "dendro_dmg_": "dendro_",
    "anemo_": "anemo_", "anemo_dmg_": "anemo_",
    "geo_": "geo_", "geo_dmg_": "geo_",
    "phys_": "phys_", "physical_dmg_": "phys_",

    "healing_": "healing_", "heal_": "healing_"
}
sub_stat_rolls = [1, 0.9, 0.8, 0.7]


possible_sub_stats = {
    "hp":        {"max_roll": 298.75, "weight": 6},
    "hp_":       {"max_roll": .0583,   "weight": 4},
    "atk":       {"max_roll": 19.45,  "weight": 6},
    "atk_":      {"max_roll": .0583,   "weight": 4},
    "def":       {"max_roll": 23.15,  "weight": 6},
    "def_":      {"max_roll": .0729,   "weight": 4},
    "crit_dmg":  {"max_roll": .0777,   "weight": 3},
    "crit_rate": {"max_roll": .0389,   "weight": 3},
    "em":        {"max_roll": 23.31,  "weight": 4},
    "er_":       {"max_roll": .0648,   "weight": 4}
}
possible_main_stats = {
    "hp": {"max_value": 4780},
    "atk": {"max_value": 311},
    "hp_": {"max_value": .466},
    "atk_": {"max_value": .466},
    "def_": {"max_value": .583},
    "em": {"max_value": 186.5},
    "er_": {"max_value": .518},
    "crit_rate": {"max_value": .311},
    "crit_dmg": {"max_value": .622},
    "healing_": {"max_value": .359},
    "pyro_": {"max_value": .466},
    "electro_": {"max_value": .466},
    "cryo_": {"max_value": .466},
    "hydro_": {"max_value": .466},
    "dendro_": {"max_value": .466},
    "anemo_": {"max_value": .466},
    "geo_": {"max_value": .466},
    "phys_": {"max_value": .583},
}

main_stat_prob = {
    "flower":  {"hp": 1},
    "plume":   {"atk": 1},
    "sands":   {"hp_": .2668, "atk_": .2666, "def_": .2666, "er_": .1, "em": .1},
    "goblet":  {"hp_": .1925, "atk_": .1925, "def_": .19, "em": .025, "pyro_": .05, "electro_": .05, "cryo_": .05, "hydro_": .05, "dendro_": .05, "anemo_": .05, "geo_": .05, "phys_": .05},
    "circlet": {"hp_": .22, "atk_": .22, "def_": .22, "crit_rate": .1, "crit_dmg": .1, "healing_": .1, "em": .04}
}

weapons = {
    'homa': {'atk': 608, 'crit_dmg': .662},
    'mist_splitter': {'atk': 674, 'crit_dmg': .441}
}


def load_json_data(path):
    with open(path, "r") as file:
        return json.load(file)


def tabulate_artifacts(artifacts):
    artifact_list = []
    for artifact in artifacts:
        row = dict()
        row["set"] = artifact["setKey"]
        row["rarity"] = artifact["rarity"]
        row["level"] = artifact["level"]
        row["slot"] = artifact["slotKey"]
        row["main_stat"] = stat_name_mapping[artifact["mainStatKey"]]
        row["main_stat_value"] = get_main_stat_value(
            stat_name_mapping[artifact["mainStatKey"]],
            artifact["level"]
        )
        row["location"] = artifact["location"]

        substats = dict()
        for substat in artifact["substats"]:
            key = stat_name_mapping[substat["key"]]
            substats[key] = substat["value"] / 100 if "_" in key else substat["value"]
        for key, item in possible_sub_stats.items():
            row[key] = 0 if key not in substats.keys() else substats[key]
        artifact_list.append(row)
    return pd.DataFrame(artifact_list)


def char_dmg(
        talent_,
        char_atk, wep_atk, atk_, flat_atk,
        dmg_bonus_,
        crit_rate, crit_dmg,
        em, reaction=Reactions.NONE, reaction_bonus=0.0,
        def_redu=0.0,
        buffs=None
):
    if buffs is None:
        buffs = []

    base_atk = (char_atk + wep_atk)
    for buff in buffs:
        talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu = buff(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction, reaction_bonus, def_redu)
    return reaction.calc_dmg(talent_, base_atk, atk_, flat_atk, crit_rate, crit_dmg, dmg_bonus_, em, reaction_bonus, def_redu)


def load_char_data(path):
    char_data = pd.read_csv(path)
    char_data.set_index("Name", inplace=True)
    char_data["HP"] = pd.to_numeric(char_data["HP"].replace(",", "", regex=True))

    def percent_to_dec(value: str):
        if "%" in value:
            value = value.replace("%", "")
            value = str(float(value) / 100)
        return value

    char_data["Ascension Stat"] = pd.to_numeric(char_data["Ascension Stat"].apply(percent_to_dec))
    return char_data


def load_artifact_main_stat_data(path):
    artifact_data = pd.read_csv(path)
    artifact_data.set_index("stat", inplace=True)
    artifact_data = artifact_data.transpose()
    percent_columns = [
        "HP%", "ATK%", "DEF%",
        "Energy Recharge%",
        "Physical DMG%", "Elemental DMG%",
        "Crit Rate%", "Crit DMG%", "Healing Bonus%"
    ]
    for col_name in percent_columns:
        artifact_data[col_name] = artifact_data[col_name] / 100
    return artifact_data


main_stat_data = load_artifact_main_stat_data("resources/genshin_data/artifact_main_stat.csv")


def get_main_stat_value(stat, level):
    main_stat_map = {
        "hp": "HP", "atk": "ATK",
        "hp_": "HP%", "atk_": "ATK%", "def_": "DEF%",
        "er_": "Energy Recharge%", "em": "Elemental Mastery",
        "pyro_": "Elemental DMG%", "electro_": "Elemental DMG%", "cryo_": "Elemental DMG%", "hydro_": "Elemental DMG%", "dendro_": "Elemental DMG%", "anemo_": "Elemental DMG%", "geo_": "Elemental DMG%", "phys_": "Elemental DMG%",
        "crit_rate": "Crit Rate%", "crit_dmg": "Crit DMG%", "healing_": "Healing Bonus%"
    }

    return main_stat_data[main_stat_map[stat]]["+" + str(level)]


def calc_dmg(character, char_artifacts, weapon, char_data):
    """
    Calculates a damage number that is used as a heuristic for how good an artifact is
    :param character:
    :param char_artifacts:
    :param weapon:
    :param char_data:
    :return:
    """
    crit_dmg = char_base_crit_dmg + weapon['crit_dmg'] if 'crit_dmg' in weapon.keys() else 0
    crit_rate = char_base_crit_rate + weapon['crit_rate'] if 'crit_rate' in weapon.keys() else 0
    # char data
    char_atk = char_data.loc[character]["ATK"]
    atk_ = char_data.loc[character]["Ascension Stat"] + weapon['atk_'] if 'atk_' in weapon.keys() else 0
    flat_atk = 0
    dmg_ = 0
    em = 0 + weapon['em'] if 'em' in weapon.keys() else 0

    atk_wep = weapon['atk']

    # Main stats
    flat_atk += char_artifacts.loc[char_artifacts['main_stat'] == "atk"]["main_stat_value"].values[0]
    atk_ += 0 if 'atk_' not in char_artifacts['main_stat'].unique() else char_artifacts.loc[char_artifacts['main_stat'] == "atk_"]["main_stat_value"].values[0]
    dmg_ += 0 if 'electro_' not in char_artifacts['main_stat'].unique() else char_artifacts.loc[char_artifacts['main_stat'] == "electro_"]["main_stat_value"].values[0]
    em += 0 if 'em' not in char_artifacts['main_stat'].unique() else char_artifacts.loc[char_artifacts['main_stat'] == "em"]["main_stat_value"].values[0]

    crit_dmg += 0 if 'crit_dmg' not in char_artifacts['main_stat'].unique() else char_artifacts.loc[char_artifacts['main_stat'] == "crit_dmg"]["main_stat_value"].values[0]
    crit_rate += 0 if 'crit_rate' not in char_artifacts['main_stat'].unique() else char_artifacts.loc[char_artifacts['main_stat'] == "crit_rate"]["main_stat_value"].values[0]

    # Sub stats
    flat_atk += char_artifacts["atk"].sum()
    atk_ += char_artifacts["atk_"].sum()
    crit_dmg += char_artifacts["crit_dmg"].sum()
    crit_rate += char_artifacts["crit_rate"].sum()
    em += char_artifacts["em"].sum()

    buffs = [
        vv_4p, sucrose_a1, sucrose_a4,
        thundering_fury_2p, thundering_fury_4p,
        mistsplitter_builder(2)
    ]
    n = char_dmg(.81, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, buffs=buffs)
    c_1_agg = char_dmg(1.51, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, reaction=Reactions.AGG, reaction_bonus=0.2, buffs=buffs)
    c_1 = char_dmg(1.51, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, buffs=buffs)
    c_2 = char_dmg(1.51, char_atk, atk_wep, atk_, flat_atk, dmg_, crit_rate, crit_dmg, em, buffs=buffs)

    return (n + c_1_agg + c_2) + (n + c_1 + c_2)


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
        for sub_stat in possible_sub_stats.keys():
            if sub_stat in artifact['sub_stats']:
                continue
            # for rv in sub_stat_rolls:
            #     possibility = copy.deepcopy(artifact)
            #     possibility['sub_stats'][sub_stat] = possible_sub_stats[sub_stat]['max_roll'] * rv
            #     possibilities.append(possibility)
            possibility = copy.deepcopy(artifact)
            possibility['sub_stats'][sub_stat] = possible_sub_stats[sub_stat]['max_roll'] * .85
            possibilities.append(possibility)
    else:
        # Add roll
        for sub_stat in artifact['sub_stats']:
            # for rv in sub_stat_rolls:
            #     possibility = copy.deepcopy(artifact)
            #     possibility['sub_stats'][sub_stat] += possible_sub_stats[sub_stat]['max_roll'] * rv
            #     possibilities.append(possibility)
            possibility = copy.deepcopy(artifact)
            possibility['sub_stats'][sub_stat] += possible_sub_stats[sub_stat]['max_roll'] * .85
            possibilities.append(possibility)
    # Recursion
    res = []
    for possibility in possibilities:
        for final_pos in all_possibilities(possibility, rolls_left - 1):
            res.append(final_pos)
    return res


def get_value(args):
    """
    Gets the damage a character would do with a specific artifact
    Users only one param as this is made to be run in parallel
    :param args:
    :return:
    """
    option = args['option']
    possible_sub_stats = args['possible_sub_stats']
    fixed_artifacts = args['fixed_artifacts']
    weapon = args['weapon']
    char_data = args['char_data']

    # Rebuild the row
    for sub_stat in possible_sub_stats.keys():
        if sub_stat in option['sub_stats']:
            option[sub_stat] = option['sub_stats'][sub_stat]
        else:
            option[sub_stat] = 0.0
    option.pop('sub_stats')

    # Add row back to calc max value
    char_artifacts = fixed_artifacts.copy()
    char_artifacts.loc[len(char_artifacts.index)] = option

    return calc_dmg('Keqing', char_artifacts, weapon, char_data)


if __name__ == '__main__':
    pool = multiprocessing.Pool(8)

    account_data = load_json_data("resources/account_data/genshinData_GOOD_2024_04_17_23_34.json")

    artifacts = account_data["artifacts"]
    artifacts_df = tabulate_artifacts(artifacts)

    char_data = load_char_data("resources/genshin_data/genshin_char_data_4_1.csv")

    character = 'KukiShinobu'
    set = 'ThunderingFury'

    char_artifacts = artifacts_df.loc[artifacts_df["location"] == character]

    results = {}
    for slot_to_optimize in ['flower', 'plume', 'sands', 'circlet', 'goblet']:
        print('***' + slot_to_optimize + '***')
        fixed_artifacts = char_artifacts.loc[char_artifacts['slot'] != slot_to_optimize]

        if slot_to_optimize == 'goblet':
            tf_artifacts = artifacts_df[(artifacts_df['main_stat'] == 'electro_') & (artifacts_df['slot'] == slot_to_optimize)].to_dict('records')
        else:
            tf_artifacts = artifacts_df[(artifacts_df['set'] == set) & (artifacts_df['slot'] == slot_to_optimize)].to_dict('records')

        calced_artifacts = []
        for idx, artifact in enumerate(tf_artifacts):
            print('calculating: {idx}/{total}'.format(idx=idx + 1, total=len(tf_artifacts)))
            rolls_left = 5 - math.floor(artifact['level'] / 4)
            # convert artifact to find all possibilities
            artifact['main_stat_value'] = possible_main_stats[artifact['main_stat']]['max_value']
            artifact['sub_stats'] = {}
            for sub_stat in possible_sub_stats.keys():
                if artifact[sub_stat] != 0:
                    artifact['sub_stats'][sub_stat] = artifact[sub_stat]
                artifact.pop(sub_stat)

            # Find all possible options when leveling up the artifact
            options = all_possibilities(copy.deepcopy(artifact), rolls_left)

            args = [{
                'option': option,
                'possible_sub_stats': possible_sub_stats,
                'fixed_artifacts': fixed_artifacts,
                'weapon': weapons['homa'],
                'char_data': char_data
            } for option in options]
            values = list(tqdm(pool.imap(get_value, args), total=len(args)))
            # values = [get_value(arg) for arg in tqdm(args)]

            artifact['avg_value'] = sum(values) / len(values)
            calced_artifacts.append(artifact)
        results[slot_to_optimize] = pd.DataFrame(calced_artifacts)
    with ExcelWriter('output/{char}_{set}.xlsx'.format(char=character, set=set)) as writer:
        for slot, df in results.items():
            df.to_excel(writer, slot)
        pd.concat([frame for frame in results.values()], axis=0).to_excel(writer, 'Combine')
    print("Done")


