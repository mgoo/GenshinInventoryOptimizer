import random
import os

from flask import Flask, render_template, render_template_string, url_for, request, jsonify

from characters import Account
from genshin_data import readable, readable_value

from optimizer import optimize as opti
from optimization_targets import Target

account_root = os.path.join('resources', 'account_data')
account_files = os.listdir(account_root)

app = Flask('InventoryOptimizer')

@app.route('/accounts')
def root():
    account_file_details = []
    for idx, account_file in enumerate(account_files):
        account_file_details.append({
            'time': os.path.getmtime(os.path.join(account_root, account_file)),
            'name': account_file.split('.')[0],
            'idx': idx
        })

    return render_template('account_list.html', account_files=account_file_details)

@app.route('/account/<id>')
def account(id):
    id = int(id)
    account = Account(os.path.join(account_root, account_files[id]))
    characters = account.characters.values()
    img_urls = []
    arti_urls = []
    wep_urls = []
    for character in characters:
        root_path = os.path.join('static', 'img', 'stickers', character.name.lower())
        try:
            options = os.listdir(root_path)
        except FileNotFoundError:
            os.mkdir(root_path)
            options = []

        if len(options) > 0:
            img_urls.append('img/stickers/' + character.name.lower() + '/' + random.choice(options))
        else:
            img_urls.append('img/noimg.jpg')

        if character.artifacts['flower'] is not None:
            arti_urls.append(character.artifacts['flower'].get_img())
        else:
            arti_urls.append('img/noimg.jpg')

        wep_urls.append(character.weapon.get_img())

    return render_template('account.html', characters=zip(characters, img_urls, arti_urls, wep_urls), readable=readable, readable_value=readable_value, account_id=id)


@app.route('/character/<account_id>/<character_id>')
def character(account_id, character_id):
    account_id = int(account_id)
    account = Account(os.path.join(account_root, account_files[account_id]))
    character = account.characters[character_id]

    char_stats = character.get_stats()

    non_zero_stats = char_stats.get_non_zero().keys()
    display_stats = ['em', 'crit_rate', 'crit_dmg'] +\
                    [stat for stat in ['heal_', 'pyro_', 'hydro_', 'dendro_', 'electro_', 'anemo_', 'cryo_', 'geo_', 'phys_'] if stat in non_zero_stats]

    sets = list({set.set_key for set in account.artifacts.values()})
    sets.sort()

    targets = [(sub_cls.__name__, sub_cls()) for sub_cls in Target.__subclasses__() if character_id == sub_cls().main_character()]
    targets.sort()

    return render_template(
        'character.html',
        character=character, stats=char_stats, display_stats=display_stats,
        account_id=account_id, character_id=character_id,
        sets=sets, targets=targets,
        readable=readable, readable_value=readable_value
    )


@app.route('/optimize/<account_id>/<character_id>')
def optimize(account_id, character_id):
    account_id = int(account_id)
    account = Account(os.path.join(account_root, account_files[account_id]))
    character = account.characters[character_id]

    arti_set = request.args.get('arti_set')
    offset_slot = request.args.get('offset_slot')
    target_name = request.args.get('target')

    target = None
    for sub_cls in Target.__subclasses__():
        if target_name == sub_cls.__name__:
            target = sub_cls()
            break

    if target is None:
        raise Exception("Target not found: " + target_name)

    results = opti(target, account, character, arti_set, offset_slot)

    ordered_weapons = results[0]
    ordered_flowers = results[1]
    ordered_plumes = results[2]
    ordered_sands = results[3]
    ordered_goblets = results[4]
    ordered_circlets = results[5]

    dmg_hist = results[6]

    weapon_weights_hist = results[7]
    flower_weights_hist = results[8]
    plume_weights_hist = results[9]
    sands_weights_hist = results[10]
    goblet_weights_hist = results[11]
    circlet_weights_hist = results[12]

    weapon_weights_grad_hist = results[13]
    flower_weights_grad_hist = results[14]
    plume_weights_grad_hist = results[15]
    sands_weights_grad_hist = results[16]
    goblet_weights_grad_hist = results[17]
    circlet_weights_grad_hist = results[18]

    wep_template = '{% from "partials/weapon_card.html" import weapon_card %} {{weapon_card(readable, readable_value, weapon)}}'
    arti_template = '{% from "partials/artifact_card.html" import artifact_card %} {{artifact_card(readable, readable_value, slot, arti)}}'

    weapon_html = render_template_string(wep_template, weapon=ordered_weapons[0][0], readable=readable, readable_value=readable_value)
    flower_html = render_template_string(arti_template, slot='flower', arti=ordered_flowers[0][0], readable=readable, readable_value=readable_value)
    plume_html = render_template_string(arti_template, slot='plume', arti=ordered_plumes[0][0], readable=readable, readable_value=readable_value)
    sands_html = render_template_string(arti_template, slot='sands', arti=ordered_sands[0][0], readable=readable, readable_value=readable_value)
    goblet_html = render_template_string(arti_template, slot='goblet', arti=ordered_goblets[0][0], readable=readable, readable_value=readable_value)
    circlet_html = render_template_string(arti_template, slot='circlet', arti=ordered_circlets[0][0], readable=readable, readable_value=readable_value)

    return jsonify(
        best_loadout=weapon_html+flower_html+plume_html+sands_html+goblet_html+circlet_html
    )


if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)
