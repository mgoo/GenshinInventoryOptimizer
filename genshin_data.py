from enum import Enum

import pandas as pd

from utils import percent_to_dec


class GenshinData:

    avg_artifact_num = 1.065
    three_line_percent_domain = .8
    three_line_percent_strong_box = .66

    char_base_crit_rate = .05
    char_base_crit_dmg = .5

    stat_name_mapping = {
        "hp":  ["HP"],  "hp_":  ["HP%"],
        "atk": ["ATK"], "atk_": ["ATK%"],
        "def": ["DEF"], "def_": ["DEF%"],
        "crit_dmg":  ["Crit DMG%", "critDMG_", "CRIT DMG", "CRITDMG"],
        "crit_rate": ["Crit Rate%", "critRate_", "CRIT Rate", "CRITRate"],
        "em":  ["Elemental Mastery", "eleMas", "ElementalMastery"],
        "er_": ["Energy Recharge%", "enerRech_", "Energy Recharge", "EnergyRecharge"],

        "pyro_":    ["pyro_dmg_", "Pyro DMG"],
        "electro_": ["electro_dmg_", "Electro DMG"],
        "cryo_":    ["cryo_dmg_", "Cryo DMG"],
        "hydro_":   ["hydro_dmg_", "Hydro DMG"],
        "dendro_":  ["dendro_dmg_", "Dendro DMG"],
        "anemo_":   ["anemo_dmg_", "Anemo DMG"],
        "geo_":     ["geo_dmg_", "Geo DMG"],
        "phys_":    ["physical_dmg_", "Physical DMG", "PhysicalDMGBonus"],

        "healing_": ["heal_", "Healing"]
    }

    class ElementTypes(Enum):
        ALL = "all_"
        PYRO = "pyro_"
        ELECTRO = "electro_"
        CRYO = "cryo_"
        HYDRO = "hydro_"
        DENDRO = "dendro_"
        ANEMO = "anemo_"
        GEO = "geo_"
        PHYS = "phys_"

    element_types = [_.value for _ in ElementTypes]

    @staticmethod
    def fix_stat_name(stat):
        # if stat name is ok
        if stat in GenshinData.stat_name_mapping:
            return stat
        # Try to find the correct name for the stat
        for key, item in GenshinData.stat_name_mapping.items():
            if stat in item:
                return key


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

    _cache_load_artifact_main_stat_data = dict()

    @staticmethod
    def tabulate_artifacts(artifacts):
        artifact_list = []
        for artifact in artifacts:
            row = dict()
            row["set"] = artifact["setKey"]
            row["rarity"] = artifact["rarity"]
            row["level"] = artifact["level"]
            row["slot"] = artifact["slotKey"]
            row["main_stat"] = GenshinData.fix_stat_name(artifact["mainStatKey"])
            row["main_stat_value"] = GenshinData.get_main_stat_value(
                GenshinData.fix_stat_name(artifact["mainStatKey"]),
                artifact["level"]
            )
            row["location"] = artifact["location"]

            substats = dict()
            for substat in artifact["substats"]:
                key = GenshinData.fix_stat_name(substat["key"])
                substats[key] = substat["value"] / 100 if "_" in key else substat["value"]
            for key, item in GenshinData.possible_sub_stats.items():
                row[key] = 0 if key not in substats.keys() else substats[key]
            artifact_list.append(row)
        return pd.DataFrame(artifact_list)

    @staticmethod
    def load_char_data(path):
        char_data = pd.read_csv(path)
        char_data.set_index("Name", inplace=True)
        char_data["HP"] = pd.to_numeric(char_data["HP"].replace(",", "", regex=True))

        def fix_name(value: str):
            if value == 'ATK':
                return 'atk_'
            return GenshinData.fix_stat_name(value)

        char_data["Ascension Stat"] = pd.to_numeric(char_data["Ascension Stat"].apply(percent_to_dec))
        char_data["Ascension Attributes"] = char_data["Ascension Attributes"].apply(fix_name)
        return char_data

    @staticmethod
    def load_weapon_data(path):
        wep_data = pd.read_csv(path)
        wep_data.set_index("Weapon", inplace=True)

        def fix_name(value: str):
            if value == 'ATK':
                return 'atk_'
            if value == 'HP':
                return 'hp_'
            if value == 'DEF':
                return 'def_'
            return GenshinData.fix_stat_name(value)

        wep_data['Value'] = pd.to_numeric(wep_data['Value'].apply(percent_to_dec))
        wep_data['Secondary'] = wep_data['Secondary'].apply(fix_name)
        return wep_data

    @staticmethod
    def get_artifact_main_stat_data(path):
        if path in GenshinData._cache_load_artifact_main_stat_data:
            return GenshinData._cache_load_artifact_main_stat_data[path]
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
        GenshinData._cache_load_artifact_main_stat_data[path] = artifact_data
        return artifact_data



    @staticmethod
    def get_main_stat_value(stat, level):
        main_stat_map = {
            "hp": "HP", "atk": "ATK",
            "hp_": "HP%", "atk_": "ATK%", "def_": "DEF%",
            "er_": "Energy Recharge%", "em": "Elemental Mastery",
            "pyro_": "Elemental DMG%", "electro_": "Elemental DMG%", "cryo_": "Elemental DMG%", "hydro_": "Elemental DMG%", "dendro_": "Elemental DMG%", "anemo_": "Elemental DMG%", "geo_": "Elemental DMG%", "phys_": "Elemental DMG%",
            "crit_rate": "Crit Rate%", "crit_dmg": "Crit DMG%", "healing_": "Healing Bonus%"
        }

        main_stat_data = GenshinData.get_artifact_main_stat_data("resources/genshin_data/artifact_main_stat.csv")

        return main_stat_data[main_stat_map[stat]]["+" + str(level)]

    @staticmethod
    def dictionise_row(artifact):
        artifact['sub_stats'] = dict()
        for sub_stat in GenshinData.possible_sub_stats.keys():
            if artifact[sub_stat] != 0:
                artifact['sub_stats'][sub_stat] = artifact[sub_stat]
            artifact.pop(sub_stat)
        return artifact

