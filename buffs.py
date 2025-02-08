from characters import Character
from stat_block import StatBlock


# Characters
def bennett_builder(bennett: Character, c1=False):
    def bennett_buff(stat_block: StatBlock):
        ratio = 1.12  # TODO assumes lv 12
        if c1:
            ratio += 0.2
        stat_block = stat_block.add('atk', ratio * (bennett.stat_block['base_atk'] + bennett.weapon.stat_block['base_atk']))
        return stat_block
    return bennett_buff


def sucrose_a1(stat_block: StatBlock):
    return stat_block.add('em', 50)


def sucrose_a4_builder(sucrose: Character, buffs=list()):
    def sucrose_a4(stat_block: StatBlock):
        return stat_block.add('em', sucrose.get_stats(buffs)['em'] * 0.2)
    return sucrose_a4


def collei_c4(stat_block: StatBlock):
    return stat_block.add('em', 60)


def nahida_a1_builder(highest_em_char, buffs=list()):
    def nahida_a1(stat_block: StatBlock):
        return stat_block.add('em', min(highest_em_char.get_stats(buffs)['em'] * 0.25, 250))
    return nahida_a1


def alhaitham_a4_builder(alhaitham: Character, buffs=list()):
    def alhaitham_a4(stat_block: StatBlock):
        bonus = 0.001 * stat_block['em']

        return stat_block + StatBlock({'s_': bonus, 'b_': bonus})
    return alhaitham_a4


def tighnari_c1(stat_block: StatBlock):
    return stat_block.add('crit_rate', 0.15)


def tighnari_c2(stat_block: StatBlock):
    return stat_block.add('dendro_', 0.2)


def tighnari_a4_builder(tighnari: Character, buffs=list()):
    def tighnari_a4(stat_block: StatBlock):
        bonus = min(tighnari.get_stats(buffs)['em'] * 0.0006, 0.6)
        return stat_block + StatBlock({'c_': bonus, 'b_': bonus})
    return tighnari_a4


def tighnari_a1(stat_block: StatBlock):
    return stat_block.add('em', 50)

def xilonen_source_sample_builder(element):
    def xilonen_source_sample(stat_block: StatBlock):
        # TODO assumes talent level 9
        return stat_block.add('def_redu_'+element.value, .33)
    return xilonen_source_sample


# Artifacts
def thundering_fury_2p(stat_block: StatBlock):
    return stat_block.add('electro_', 0.15)


def thundering_fury_4p(stat_block: StatBlock):
    return stat_block + StatBlock({
        'over_': 0.4,
        'echarg_': 0.4,
        'scond_': 0.4,
        'hbloom_': 0.4,
        'agg_': 0.2
    })


def vv_4p_builder(element):
    def vv_4p(stat_block: StatBlock):
        return stat_block.add('def_redu_' + element.value, 0.4)
    return vv_4p


def wandererstroupe_2p(stat_block: StatBlock):
    return stat_block.add('em', 80)


def wandererstroupe_4p(stat_block: StatBlock):
    return stat_block.add('c_', 0.35)


def deepwood_2p(stat_block: StatBlock):
    return stat_block.add('dendro_', 0.15)


def deepwood_4p(stat_block: StatBlock):
    return stat_block.add('def_redu_dendro_', 0.3)


def gildeddreams_2p(stat_block: StatBlock):
    return stat_block.add('em', 80)


def gildeddreams_4p_builder(same, diff):
    def gilded_dreams_4p(stat_block: StatBlock):
        return stat_block + StatBlock({
            'atk_': 0.14 * min(same, 3),
            'em_': 50 * min(diff, 3)
        })
    return gilded_dreams_4p


def cinder_city_4p_builder(is_nightsoul_blessing):
    def cinder_city_4p(stat_block: StatBlock):
        if is_nightsoul_blessing:
            return stat_block.add('elem_', 0.12 + 0.28)
        else:
            return stat_block.add('elem_', 0.12)
    return cinder_city_4p

# Weapons
def mistsplitter_builder(stacks):
    def mistsplitter_buff(stat_block: StatBlock):
        amounts = [0.08, 0.16, 0.28]
        total_boost = 0.12 + amounts[stacks]
        return stat_block.add('elem_', total_boost)
    return mistsplitter_buff


def thousand_dreams_builder(same):
    def thousand_dreams(stat_block: StatBlock):
        if same:
            return stat_block.add('em', 32)
        else:
            # TODO DMG bonus for only the characters type (this is close enough for now
            return stat_block.add('elem_', 0.1)
    return thousand_dreams


def foliar_incision_builder(char: Character, buffs=list()):
    def foliar_incision(stat_block: StatBlock):
        return stat_block + StatBlock({
            'crit_rate': 0.04,
            'dmg': char.get_stats(buffs)['em'] * 1.2
        })
    return foliar_incision


def stringless(stat_block: StatBlock):
    return stat_block + StatBlock({
        's_': 0.48,
        'b_': 0.48
    })


#Resonance
def pyro_res(stat_block: StatBlock):
    return stat_block.add('atk_', 0.25)


def cryo_res(stat_block: StatBlock):
    return stat_block.add('crit_rate', 0.15)


def geo_res(stat_block: StatBlock):
    # TODO elemental defence reduction
    return stat_block
    # dmg_.add_bonus(0.15, GenshinData.ElementTypes.ALL)
    # def_redu += 0.2
    # return talent_, atk_,  flat_atk, hp_, flat_hp, def_, flat_def, flat_dmg, crit_rate, crit_dmg, em


def dendro_res_builder(after_primary, after_secondary):
    em_bonus = 50
    if after_primary:
        em_bonus += 30
    if after_secondary:
        em_bonus += 20

    def dendro_res(stat_block: StatBlock):
        return stat_block.add('em', em_bonus)
    return dendro_res
