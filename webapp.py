import random
import os

from flask import Flask, render_template, url_for

from characters import Account
from genshin_data import readable, readable_value

app = Flask('InventoryOptimizer')

@app.route('/')
def root():
    return '<h1>UwU</h1>'

@app.route('/account')
def account():
    account = Account("resources/account_data/genshinData_GOOD_2024_04_22_20_23.json")
    characters = account.characters.values()
    img_urls = []
    arti_urls = []
    wep_urls = []
    for character in characters:
        root_path = os.path.join('static', 'img', 'stickers', character.name.lower())
        try:
            options = os.listdir(root_path)
        except FileNotFoundError:
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

    return render_template('account.html', characters=zip(characters, img_urls, arti_urls, wep_urls), readable=readable, readable_value=readable_value)

@app.route('/character/<id>')
def character(id):
    account = Account("resources/account_data/genshinData_GOOD_2024_04_22_20_23.json")
    character = account.characters[id]

    char_stats = character.get_stats()

    non_zero_stats = char_stats.get_non_zero().keys()
    display_stats = ['em', 'crit_rate', 'crit_dmg'] +\
                    [stat for stat in ['heal_', 'pyro_', 'hydro_', 'dendro_', 'electro_', 'anemo_', 'cryo_', 'geo_', 'phys_'] if stat in non_zero_stats]

    return render_template('character.html', character=character, stats=char_stats, display_stats=display_stats, readable=readable, readable_value=readable_value)

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True)