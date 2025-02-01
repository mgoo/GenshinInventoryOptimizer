import os
from collections import defaultdict

from genshin_data import GenshinData
from stat_block import StatBlock


class Artifact:

    artifact_locations = defaultdict(lambda: list())

    @classmethod
    def from_raw(cls, raw_artifact):
        art_id = int(raw_artifact["id"])
        if art_id > GenshinData.max_artifact_id:
            GenshinData.max_artifact_id = art_id

        location = raw_artifact["location"]

        sub_stats = dict()
        for sub_stat in raw_artifact["substats"]:
            key = GenshinData.fix_stat_name(sub_stat["key"])
            sub_stats[key] = sub_stat["value"] / 100 if "_" in key else sub_stat["value"]

        artifact = cls(
            art_id,
            raw_artifact['setKey'], raw_artifact["slotKey"],
            raw_artifact["level"], GenshinData.fix_stat_name(raw_artifact["mainStatKey"]),
            sub_stats, raw_artifact['rarity'],
        )
        if location != '':
            artifact.add_location(location)
        return artifact

    def __init__(self, id, set_key, slot_key, lv, main_stat, sub_stats, rarity):
        self.id = id
        self.set_key = set_key
        self.slot_key = slot_key
        self.lv = lv
        self.main_stat = main_stat
        self.main_stat_value = GenshinData.get_main_stat_value(self.main_stat, self.lv)
        self.sub_stats = sub_stats
        self.rarity = rarity
        self.locations = []

    def sub_stat_block(self):
        return StatBlock(self.sub_stats)

    def main_stat_block(self):
        value = self.main_stat_value
        stat_block = StatBlock({self.main_stat: value})
        return stat_block

    def total_stat_boost(self):
        return self.main_stat_block() + self.sub_stat_block()

    def get_img(self):
        filename = None
        with open(os.path.join('static', 'assets', 'artifacts', self.set_key, 'index.ts'), 'r') as file:
            for line in file.readlines():
                if line.startswith('import ' + self.slot_key):
                    filename = line.split('\'')[1][2:]
                    break
        if filename is None:
            print('cri')
        return 'assets/artifacts/' + self.set_key + '/' + filename

    def add_location(self, loc):
        self.locations.append(loc)
        Artifact.artifact_locations[loc].append(self)
