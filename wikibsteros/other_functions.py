"""other functions"""
import datetime
import random
import os
import pandas as pd
import requests, json, itertools
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from .models import Character

def days_between(d1, d2):
    """ difference between two dates """
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def situation_in_the_crowns():
    # days passed bran
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    bran_stark_days = sansa_stark_days = tyrion_days = bronn_days = \
    (days_between(dt_string, '2019-05-19'))
    prince_of_dorne_days = yara_days = (days_between(dt_string, '2019-04-15'))
    edmure_days = (days_between(dt_string, '2017-07-17'))
    gendry_days = (days_between(dt_string, '2019-05-06'))
    robin_days = (days_between(dt_string, '2014-09-27'))
    days_passed = [bran_stark_days, sansa_stark_days, prince_of_dorne_days, edmure_days,
                   tyrion_days, yara_days, bronn_days, gendry_days, robin_days]
    names_sovereings = ['Bran Stark', 'Sansa Stark', 'Prince of Dorne', 'Edmure Tully',
                        'Tyrion Lannister', 'Yara Greyjoy', 'Bronn', 'Gendry Baratheon',
                        'Robin Arryn']

    names_houses = ['Stark', 'Stark', 'Martell', 'Tully', 'Lannister', 'Greyjoy',
                    _('Bronn‘s house of Highgarden'), 'Baratheon', 'Arryn']

    names_regions = [_('First of His Name, King of the Andals and the First Men, Protector \
                    of the Seven Kingdoms'), _('The Kingdom of the North'),
                     _('The Principality of Dorne'), _('The Riverlands'),
                     _('The Westerlands'), _('The Salt Throne'), _('The Reach'),
                     _('The Kingdom of the Stormlands'), _('Kingdom of Mountain and Vale')]

    names_images = ['7789657045_bran-stark-dans-la-saison-7-de-game-of-thrones.png',
                    '4723856-sophie-turner-dans-la-saison-7-de-game-950x0-1.jpg',
                    'SEI_68448418.jpg',
                    '6ff0c108885366ade073c109fde3e9abde06d777_00.jpg', 'theory-1553634761.jpg',
                    'yara.jpeg', 'bronn.jpeg', 'game-of-thrones-joe-dempsie.jpg',
                    'Robin-Arryn-Game-Thrones-Finale.jpg']

    names_landscapes = ['Iron_throne.jpg', 'Winterfell-white-raven.jpg', 'HI_115201.jpg',
                        'main-qimg-2b69712c18af3367c3d2b40c1e6f2472.png', 'casterly-rock.png', 
                        'Pyke.jpg',
                        '704_Highgarden.png', 'siege-of-storm-s-end-during-robert-s-rebellion.jpg',
                        'xlarge5331a9e3ef459@2x.png']
    return days_passed, names_sovereings, names_houses, names_regions, names_images, \
    names_landscapes

def choose_a_region():
    """ the user can choose his native region """
    try:
        req = requests.get("https://api.got.show/api/show/regions")
        result = json.loads(req.text)
        a = list()
        a.append((0, _('----- CHOOSE A REGION -----')))
        for i in itertools.count():
            try:
                a.append((result[i]['name'], result[i]['name']))
            except:
                break
        list_of_regions = tuple(x for x in a)
    except:
        list_of_regions = ()
    return list_of_regions

def choose_a_house():
    """ the user can choose his allegiance """
    try:
        req = requests.get("https://api.got.show/api/show/houses")
        result = json.loads(req.text)
        a = list()
        a.append((0, _('----- CHOOSE A HOUSE -----')))
        for i in itertools.count():
            try:
                a.append((result[i]['name'], result[i]['name']))
            except:
                break
        list_of_houses = tuple(x for x in a)     
    except:
        list_of_houses = ()
    return list_of_houses

def choose_a_character():
    """ the user can use a character in the maggy part"""
    try:
        req = requests.get("https://api.got.show/api/show/characters")
        result = json.loads(req.text)
        a = list()
        a.append((0, _(' CHOOSE A CHARACTER')))
        for i in itertools.count():
            try:
                a.append((result[i]['name'], result[i]['name']))
            except:
                break
        list_of_characters = tuple(x for x in a)
    except:
        list_of_characters = ()
    return list_of_characters

def battle_init():
    """ a method to init the HP, atatcks of the characters """
    family_battles = [[10, random.randint(10, 12), random.randint(10, 12)],
                      [10, random.randint(10, 12), random.randint(10, 12)],
                      [140, random.randint(70, 75), random.randint(20, 22)],
                      [100, random.randint(70, 75), random.randint(40, 45)],
                      [110, random.randint(50, 55), random.randint(20, 25)],
                      [130, random.randint(40, 42), random.randint(30, 32)],
                      [150, random.randint(40, 42), random.randint(20, 25)],
                      [50, random.randint(60, 65), random.randint(50, 55)],
                      [140, random.randint(40, 45), random.randint(30, 32)],
                      [100, random.randint(60, 65), random.randint(40, 42)],
                      [999, random.randint(120, 130), 120*120],
                      [80, random.randint(50, 55), random.randint(60, 65)],
                      [100, random.randint(60, 65), random.randint(30, 32)],
                      [150, random.randint(60, 65), random.randint(20, 22)],
                      [110, random.randint(50, 55), random.randint(40, 45)],
                      [120, random.randint(50, 55), random.randint(50, 55)],
                      [130, random.randint(50, 55), random.randint(30, 32)],
                      [80, random.randint(80, 85), random.randint(10, 12)],]

    family_battles = pd.DataFrame(family_battles,
                                  columns=['Health Points', 'attack_1', 'attack2'],
                                  index=['Dude', 'Girl', 'Jon Snow', 'Ellaria Sand',
                                         'Catelyn Stark', 'Oberyn Martell', 'Littlefinger',
                                         'Olenna Tyrell', 'Melisandre', 'Ramsay Bolton',
                                         'Night King',
                                         'Tyrion', 'Ygrid', 'The Mountain', 'Yara Greyjoy',
                                         'Cersei Lannister', 'Khal Drogo', 'Daenerys Targaryen'])
    return family_battles

def battle_cards(a, b, c):
    """ a method to define the characters and the picture cards """
    #populate the dictionnary
    a = {}
    a[b[0]] = c[1]
    a[b[1]] = c[-1]
    a[b[2]] = c[4]
    a[b[3]] = c[-2]
    a[b[4]] = c[11]
    a[b[5]] = c[7]
    a[b[6]] = c[8]
    a[b[7]] = c[2]
    a[b[9]] = c[0]
    a[b[10]] = c[3]
    a[b[11]] = c[5]
    a[b[12]] = c[6]
    a[b[-2]] = c[10]
    a[b[-1]] = c[-3]
    return a

def get_cards():
    init = battle_init()
    list_characters = [f for f in init.index.values]
    # Get the current lang
    lang_web = translation.get_language()
    path = "wikibsteros/static/wikibsteros/img/cards/" + lang_web
    dirs = os.listdir(path)
    dirs.remove('dude.jpeg')
    dirs.remove('angelina.jpeg')
    list_characters.remove('Dude'),
    list_characters.remove('Girl')
    try:
        dirs.remove('.DS_Store')
    except:
        pass
    try:
        dirs.remove('king.jpg')
    except:
        pass
    dict_characters = {}
    cards = battle_cards(dict_characters, list_characters, dirs)
    return dirs, lang_web, list_characters, cards

def fight(selected, family):
    family = battle_init()
    hp_night_king = family.loc['Night King', 'Health Points']
    status_game = None
    iterations = 0
    alives = selected
    char_1_hp_list, char_2_hp_list, char_3_hp_list, char_4_hp_list, hp_night_king_list = \
    [], [], [], [], []
    char_1_hp, char_2_hp, char_3_hp, char_4_hp = family.loc[selected[0], 'Health Points'], \
    family.loc[selected[1], 'Health Points'], \
    family.loc[selected[2], 'Health Points'], family.loc[selected[3], 'Health Points']
    while hp_night_king >= 0:
        iterations += 1
        random_attack_lists = ['attack_1', 'attack2']
        random_attack = []
        for i in range(0, 4):
            random_attack.append(random.choice(random_attack_lists))
        count = []
        damage_attack_list = []
        for i in range(0, len(alives)):
            count.append(family.loc[selected[i], random_attack[i]])
            damage_attack_list.append(family.loc[alives[i], random_attack[i]])

        success_rate_night_king = round(random.uniform(0.1, 1.0), 10)
        if success_rate_night_king >= 0.6:
            attack_night_king = family.loc['Night King', random.choice(random_attack_lists)]
        else:
            attack_night_king = 0

        if char_1_hp <= 0:
            count[0] = 0
            if char_2_hp <= 0:
                count[1] = 0
                if char_3_hp <= 0:
                    count[2] = 0
                    if char_4_hp <= 0:
                        count[3] = 0
                        break
                    else: char_4_hp -= attack_night_king
                else:
                    char_3_hp -= attack_night_king
            else:
                char_2_hp -= attack_night_king
        else:
            char_1_hp -= attack_night_king

        somme = sum(count) + 10
        hp_night_king -= somme

        char_1_hp_list.append(char_1_hp)
        char_2_hp_list.append(char_2_hp)
        char_3_hp_list.append(char_3_hp)
        char_4_hp_list.append(char_4_hp)
        hp_night_king_list.append(hp_night_king)

        if char_1_hp <= 0 and char_2_hp <= 0 and char_3_hp <= 0 and char_4_hp <= 0:
            status_game = False
            break
        if hp_night_king <= 0:
            status_game = True
            break
        continue

    return selected, random_attack, iterations, status_game, char_1_hp_list, \
    char_2_hp_list, char_3_hp_list, char_4_hp_list, hp_night_king_list

def random_quote_maggy():
    g = requests.get("https://got-quotes.herokuapp.com/quotes")
    result = json.loads(g.text)
    quote = result['quote']
    character = result['character']
    return quote, character
