"""insert informations in database"""
import pytz
import datetime
import itertools
import json
import requests
from django.utils import translation
from django.contrib.auth.models import User
from wikibsteros.models import Article, Houses, Character, City
from django.utils.translation import ugettext_lazy as _
from .constants import FIRST_ARTICLE_RESUME, FIRST_ARTICLE_TITLE, SECOND_ARTICLE_TITLE, SECOND_ARTICLE_RESUME_EN, \
CROWNLANDS, REACH, SECOND_ARTICLE_RESUME_FR, SECOND_ARTICLE_RESUME_CL, NED_STARK_S_1, ELLARIA_S_5, ELLARIA_S_6, ELLARIA_S_7, ELLARIA_S_8, \
ELLARIA_S_4, SANSA_S_1, SANSA_S_2, SANSA_S_3, SANSA_S_4, SANSA_S_5, SANSA_S_6, SANSA_S_7, SANSA_S_8, SANSA_S_9, ROBB_S_1, ROBB_S_2, ROBB_S_3, \
ROBB_S_4, JORY_S_1, ROS_S_1, ROS_S_2, ROS_S_3, J_REED_S_3, J_REED_S_4, N_UMBER_S_7, N_UMBER_S_8, QHONO_S_6, QHONO_S_7, QHONO_S_8, \
ORNELLA_S_6, VALA_S_5, VALA_S_6, BITER_S_1, BITER_S_2, BITER_S_4, MARILLION_S_1, MORDANE_S_1, WYMAN_S_6, CLEY_S_6, KARSI_S_5, \
KINVARA_S_6, ZANRUSH_S_6, CRESSEN_S_2, SALLADHOR_S_2, SALLADHOR_S_3, SALLADHOR_S_4, UNELLA_S_5, UNELLA_S_6, HALLYNE_S_2, \
DONTOS_S_2, DONTOS_S_4, VANCE_C_S_4, DONNELL_S_4, TYCHO_S_4, TYCHO_S_5, TYCHO_S_7, YOREN_S_1, YOREN_S_2, STEELSHANKS_S_3, \
WOLKAN_S_6, WOLKAN_S_7, WOLKAN_S_8, MYRANDA_S_3, MYRANDA_S_4, MYRANDA_S_5, MYRANDA_S_6, TICKLER_S_2, KITTY_S_6, KITTY_S_7, \
ILLYRIO_S_1, TERNESIO_S_4, TERNESIO_S_5, THE_WAIF_S_5, THE_WAIF_S_6, MOSSADOR_S_4, MOSSADOR_S_5, MALKO_S_5, ANGUY_S_3, \
LANCEL_S_1, LANCEL_S_2, LANCEL_S_5, LANCEL_S_6, ALTON_S_2, ROBERT_S_1, MERO_S_3, KRAZNYS_S_3

class InsertObjects():
    """ fill and complete database with objects"""
    def get_the_id_from_the_char_name(name, titles):
        char = Character.objects.filter(name=name, titles=titles)
        for this_char in char:
            return this_char.id, this_char.titles

    def get_id_user(name):
        result = User.objects.filter(username=name)
        for res in result:
            return res.id

    def get_current_lang():
        """ get the langage of the web page : fr or en or cl"""
        return translation.get_language()

    def insert_articles():
        """ insert some articles to read"""
        curr_lang = InsertObjects.get_current_lang()
        bran_user = InsertObjects.get_id_user("Bran Stark")
        Article.objects.filter(id=1).update(title=_(FIRST_ARTICLE_TITLE),
                                            content=_(FIRST_ARTICLE_RESUME),
                                            autor_id=bran_user)

        sansa_user = InsertObjects.get_id_user("Sansa Stark")
        Article.objects.filter(id=2).update(title=_(SECOND_ARTICLE_TITLE),
                                            autor_id=sansa_user)
        if curr_lang == "en":
            Article.objects.filter(id=2).update(title=_(SECOND_ARTICLE_TITLE),
                                                content=SECOND_ARTICLE_RESUME_EN)
        elif curr_lang == "fr":
            Article.objects.filter(id=2).update(title=_(SECOND_ARTICLE_TITLE),
                                                content=SECOND_ARTICLE_RESUME_FR)
        else:
            Article.objects.filter(id=2).update(title=_(SECOND_ARTICLE_TITLE),
                                                content=SECOND_ARTICLE_RESUME_CL)

    def insert_users():
        """ the users can not have the same characters names"""
        secret_password = ''
        try:
            pass
        except:
            if not User.objects.all():
                req = requests.get("https://api.got.show/api/show/characters")
                result = json.loads(req.text)
                for i in itertools.count():
                    try:
                        User.objects.create_user(username=result[i]["name"], \
                            password=secret_password, email='websteros@yahoo.com')
                    except:
                        break

    def insert_characters():
        """insert characters in database"""
        try:
            pass
        except:
            if not Character.objects.all():
                req = requests.get("https://api.got.show/api/show/characters")
                result = json.loads(req.text)
                mother = 'Unknown'
                for i in itertools.count():
                    try:
                        age = result[i]["age"]["age"]
                    except:
                        age = 0
                    try:
                        died = result[i]["death"]
                    except:
                        died = 0
                    try:
                        father = result[i]["father"]
                    except:
                        father = "Unknown"
                    try:
                        playedBy = result[i]["actor"]
                    except:
                        playedBy = "Unknown"
                    try:
                        image = result[i]["image"]
                    except:
                        pass
                    try:
                        house = result[i]["house"]
                    except:
                        house = ''
                    try:
                        mother = result[i]["mother"]
                    except:
                        mother = 'Unknown'
                    try:
                        Character.objects.get_or_create(name=result[i]["name"], \
                            gender=result[i]["gender"], culture=result[i]["culture"], \
                            lovers=result[i]["lovers"], died=died,\
                            titles=result[i]["titles"], \
                            father=father, mother=mother, \
                            allegiances=result[i]["allegiances"], playedBy=playedBy, \
                            image=image, alive=result[i]["alive"],\
                            origin=result[i]["origin"], religion=result[i]["religion"], \
                            siblings=result[i]["siblings"], spouse=result[i]["spouse"], \
                            house=house, age=age)
                        print("no exception")
                    except Exception as e:
                        print(e)
                        break
        
    def get_features_char(name):
        char = Character.objects.filter(name=name)
        print(char)

    def update_char_from_database():
        """ fill and update our database, character part"""
        NP = "Character not present."
        Character.objects.filter(name="Eddard Stark").update(location="King‘s Landing", s_1=NED_STARK_S_1, s_9=NP)
        Character.objects.filter(name="Bran Stark").update(location="King‘s Landing")
        Character.objects.filter(name="Sansa Stark").update(location="Winterfell", s_1=SANSA_S_1, s_2=SANSA_S_2, s_3=SANSA_S_3, \
        s_4=SANSA_S_4, s_5=SANSA_S_5, s_6=SANSA_S_6, s_7=SANSA_S_7, s_8=SANSA_S_8, s_9=SANSA_S_9)
        Character.objects.filter(name="Catelyn Stark").update(location="The Twins")
        Character.objects.filter(name="Robb Stark").update(location="The Twins", s_1=ROBB_S_1, s_2=ROBB_S_2, \
        s_3=ROBB_S_3, s_4=ROBB_S_4)
        Character.objects.filter(name="Arya Stark").update(location="King‘s Landing")
        Character.objects.filter(name="Rickon Stark").update(location="Winterfell")
        Character.objects.filter(name="Jon Snow").update(location="Castleblack")
        Character.objects.filter(name="Benjen Stark").update(location="Lands of Always Winter")
        Character.objects.filter(name="Theon Greyjoy").update(alive=False, died=305, location="Winterfell")
        Character.objects.filter(name="Rodrik Cassel").update(location="Winterfell")
        Character.objects.filter(name="Jory Cassel").update(location="King‘s Landing", s_1=JORY_S_1)
        Character.objects.filter(name="Lyanna Mormont").update(alive=False, died=305, location="Winterfell")
        Character.objects.filter(name="Wolkan").update(location="Winterfell",
                                                    s_6=WOLKAN_S_6, s_7=WOLKAN_S_7, s_8=WOLKAN_S_8,
                                                       s_9=_("Maester Wolkan surprises Darren Blackmyre stealing a book from the library. \
                                                       He tries to find the little boy in the sacred wood but the maester is finally found hanged on the tree-heart, his body mutilated."))
        Character.objects.filter(name="Margaery Tyrell").update(location="King‘s Landing")
        Character.objects.filter(name="Loras Tyrell").update(location="King‘s Landing")
        Character.objects.filter(name="Olenna Redwyne").update(location="Highgarden")
        Character.objects.filter(name="Ellaria Sand").update(location="King‘s Landing", \
        s_4 = ELLARIA_S_4, s_5=ELLARIA_S_5, s_6=ELLARIA_S_6, s_7=ELLARIA_S_7,
        s_8=ELLARIA_S_8, s_2="This section is empty,     you can help to improve our community by adding to it." ,s_9=NP)
        Character.objects.filter(name="Cersei Lannister").update(location="King‘s Landing")
        Character.objects.filter(name="Mace Tyrell").update(location="King‘s Landing")
        Character.objects.filter(name="Myrcella Baratheon").update(location="King‘s Landing")
        Character.objects.filter(name="Joffrey Baratheon").update(location="King‘s Landing")
        Character.objects.filter(name="Tommen Baratheon").update(location="King‘s Landing")
        Character.objects.filter(name="Roose Bolton").update(location="Winterfell")
        Character.objects.filter(name="Ramsay Snow").update(location="Winterfell")
        Character.objects.filter(name="Myranda").update(location="Winterfell", s_9="")
        Character.objects.filter(name="Euron Greyjoy").update(location="King‘s Landing", s_9="")
        Character.objects.filter(name="Aeron Greyjoy").update(location="Pyke (castle)", s_9="")
        Character.objects.filter(name="Samwell Tarly").update(location="King‘s Landing", s_9="")
        Character.objects.filter(name="Gilly").update(location="King‘s Landing", s_9="")
        Character.objects.filter(name="Ros").update(location="King‘s Landing", s_1=ROS_S_1, s_2=ROS_S_2, s_3=ROS_S_3)
        Character.objects.filter(name="Jojen Reed").update(location="The North", s_3=J_REED_S_3, s_4=J_REED_S_4)
        Character.objects.filter(name="Ned Umber").update(location="Last Hearth", s_7=N_UMBER_S_7, s_8=N_UMBER_S_8)
        Character.objects.filter(name="Qhono").update(location="Winterfell", s_6=QHONO_S_6, s_7=QHONO_S_7, s_8=QHONO_S_8)
        Character.objects.filter(name="Ornela").update(location="Vaes Dothrak", s_6=ORNELLA_S_6)
        Character.objects.filter(name="Vala").update(location="Pentos", s_5=VALA_S_5, s_6=VALA_S_6)
        Character.objects.filter(name="Biter").update(location="The Riverlands", s_1=BITER_S_1, \
        s_2=BITER_S_2, s_4=BITER_S_4)
        Character.objects.filter(name="Marillion").update(location="King‘s Landing", s_1=MARILLION_S_1)
        Character.objects.filter(name="Mordane").update(location="King‘s Landing", s_1=MORDANE_S_1)
        Character.objects.filter(name="Wyman Manderly").update(location="Winterfell", s_6=WYMAN_S_6)
        Character.objects.filter(name="Cley Cerwyn").update(location="Winterfell", s_6=CLEY_S_6)
        Character.objects.filter(name="Karsi").update(location="Hardhome", s_5=KARSI_S_5)
        Character.objects.filter(name="Kinvara").update(location="Meereen", s_6=KINVARA_S_6)
        Character.objects.filter(name="Zanrush").update(location="Meereen", s_6=ZANRUSH_S_6)
        Character.objects.filter(name="Cressen").update(location="Dragonstone", s_2=CRESSEN_S_2)
        Character.objects.filter(name="Salladhor Saan").update(location="Dragonstone", s_2=SALLADHOR_S_2,
        s_3=SALLADHOR_S_3, s_4=SALLADHOR_S_4)
        Character.objects.filter(name="Unella").update(location="King's Landing", s_5=UNELLA_S_5,
        s_6=UNELLA_S_6)
        Character.objects.filter(name="Hallyne").update(location="King's Landing", s_2=HALLYNE_S_2)
        Character.objects.filter(name="Dontos Hollard").update(location="King's Landing", s_2=DONTOS_S_2,
        s_4=DONTOS_S_4)
        Character.objects.filter(name="Vance Corbray").update(location="The Eyrie", s_4=VANCE_C_S_4)
        Character.objects.filter(name="Donnel Waynwood").update(location="The Eyrie", s_4=DONNELL_S_4)
        Character.objects.filter(name="Yoren").update(location="The Riverlands", s_1=YOREN_S_1, s_2=YOREN_S_2)
        Character.objects.filter(name="Steelshanks").update(location="King's Landing", s_3=STEELSHANKS_S_3)
        Character.objects.filter(name="Myranda").update(location="Winterfell", s_3=MYRANDA_S_3, s_4=MYRANDA_S_4,
        s_5=MYRANDA_S_5, s_6=MYRANDA_S_6)
        Character.objects.filter(name="Tickler").update(location="Harrenhal", s_2=TICKLER_S_2)
        Character.objects.filter(name="Kitty Frey").update(location="The Twins", s_6=KITTY_S_6, s_7=KITTY_S_7)
        Character.objects.filter(name="Illyrio Mopatis").update(location="Pentos", s_1=ILLYRIO_S_1)
        Character.objects.filter(name="Ternesio Terys").update(location="Braavos", s_4=TERNESIO_S_4, s_5=TERNESIO_S_5)
        Character.objects.filter(name="The Waif").update(location="Braavos", s_5=THE_WAIF_S_5, s_6=THE_WAIF_S_6)
        Character.objects.filter(name="Mossador").update(location="Meereen", s_4=MOSSADOR_S_4, s_5=MOSSADOR_S_5)
        Character.objects.filter(name="Malko").update(location="Meereen", s_5=MALKO_S_5, s_1="This section is empty,     you can help to improve our community by adding to it.")
        Character.objects.filter(name="Anguy").update(location="The Riverlands", s_3=ANGUY_S_3)
        Character.objects.filter(name="Lancel Lannister").update(location="King‘s Landing", s_1=LANCEL_S_1, s_2=LANCEL_S_2, s_5=LANCEL_S_5, s_6=LANCEL_S_6)
        Character.objects.filter(name="Alton Lannister").update(location="The North", s_2=ALTON_S_2)
        Character.objects.filter(name="Robert Baratheon").update(location="King‘s Landing", s_1=ROBERT_S_1)
        Character.objects.filter(name="Mero").update(location="Essos", s_3=MERO_S_3)
        Character.objects.filter(name="Kraznys mo Nakloz").update(location="Astapor", s_3=KRAZNYS_S_3)

    def update_city_from_database():
        """ fill and update our database, city part"""
        City.objects.filter(name="King‘s Landing").update(population=350000, location=CROWNLANDS,
                                                          type=_("Continental Capital"),
                                                          image="kl.jpg")
        City.objects.filter(name="Oldtown").update(population=450000, location=REACH,
                                                   image="old-town-and-the-hightower.jpg")
        City.objects.filter(name="Volantis").update(population=1200000,
                                                    image="volantis.jpg")
        City.objects.filter(name="Vaes Dothrak").update(image="f2946ccd2597c1442aa8ade333feb263\
        --iron-throne-winter-is-coming.jpg")
        City.objects.filter(name="Tyrosh").update(image="tyrosh10.jpg")
        City.objects.filter(name="Braavos").update(population=800000, image="braavos.jpg")
        City.objects.filter(name="Norvos").update(population=600000)
        City.objects.filter(name="Pentos").update(population=500000)
        City.objects.filter(name="Qohor").update(population=500000)
        City.objects.filter(name="Tyrosh").update(population=400000)
        City.objects.filter(name="Astapor").update(population=300000)
        City.objects.filter(name="Myr").update(population=400000)
        City.objects.filter(name="Lys").update(population=400000)
        City.objects.filter(name="Lorath").update(population=250000)
        City.objects.filter(name="Mantarys").update(population=150000)
        City.objects.filter(name="Meereen").update(population=450000)
        City.objects.filter(name="New Ghis").update(population=600000, image="newghis.jpg")
        City.objects.filter(name="Qarth").update(population=500000)
        City.objects.filter(name="Lannisport").update(population=250000)
        City.objects.filter(name="Sunspear").update(population=90000, image="sunspear.png")
                                                                                                            
    def get_id_char():
        api = anapioficeandfire.API()
        for t in User.objects.filter(username="Ellaria Sand"):
            print(t.id)
        jon_snow = api.get_character(id=225)
        for title in jon_snow.aliases:
            print(title)

    def insert_houses():
        """insert houses of Websteros"""
        try : 
            pass
        except :
            if not Houses.objects.all():
                for i in range(1,445):
                    a = requests.get("https://anapioficeandfire.com/api/houses/" + str(i))
                    b = json.loads(a.text)
                    Houses.objects.get_or_create(name=b["name"])

    def insert_cities():
        """insert cities of Websteros"""
        try:
            pass
        except:
            req, req_2 = requests.get("https://api.got.show/api/show/castles"), \
            requests.get("https://api.got.show/api/show/cities")
            result, result_2 = json.loads(req.text), json.loads(req_2.text)
            if not City.objects.all():
                for k in itertools.count():
                    try:
                        City.objects.get_or_create(name=result_2[k]["name"], \
                                                rulers=result_2[k]["rulers"], religion=result_2[k]["religion"],
                                                location=result_2[k]["location"], founder=result_2[k]["founder"],
                                                type=result_2[k]["type"])
                    except:
                        break
                for k in itertools.count():
                    try:
                        City.objects.get_or_create(name=result[k]["name"], \
                                                rulers=result[k]["rulers"], religion=result[k]["religion"],
                                                location=result[k]["location"], founder=result[k]["founder"],
                                                type=result[k]["type"])
                    except:
                        break

class WeatherObjects():
    """ class weather for the forecasts """
    def create_dict():
        dict_real_and_got_cities = {_('Castleblack') : 'McMurdo Station', _('Winterfell') : \
                                    'Mould Bay', _('Eastwatch-by-the-Sea') : 'Qaanaaq',
                                    _('Whiteharbor') : 'Nuuk', _('The Eyrie') : 'Bern, Switzerland',
                                    _('Gulltown') : 'Geneva, Switzerland', _('The Twins') : \
                                    'Manchester, UK', _('Riverrun') : 'Amsterdam', _('Pyke') : \
                                    'Dublin', _('King‘s Landing') : 'Naples', _('Casterly Rock') : \
                                    'Berlin', _('Storm‘s End') : 'Bordeaux', _('Highgarden') : \
                                    'Milan', _('Oldtown') : 'Rome', _('Sunspear') : 'Málaga',
                                    _('Water Gardens') : 'Casabermeja', _('Hellholt') : \
                                    'Seville, Spain', 'Braavos' : 'Venice', 'Pentos' : 'Dubrovnik',
                                    'Myr' : 'Tirana', 'Tyrosh' : 'Kerkyra', 'Lys' : 'Crete',
                                    'Volantis' : 'Athens', 'Vaes Dothrak' : 'Kathmandu', 
                                    'Valyria' : 'Mecca', 'Yunkai' : 'Antalya', 'Meereen' : \
                                    'Izmir', 'Astapor' : 'Adana', 'Qarth' : 'Dubai'}
        return dict_real_and_got_cities

    def call_api():
        """ call the api OpenWeather """
        list_of_results = []
        secret_key = '3cf63bac22ea72262bb10f739247a998'
        dict_real_and_got_cities = WeatherObjects.create_dict()
        for key, value in dict_real_and_got_cities.items():
            req = requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + \
            value + "&appid=" + secret_key)
            result = json.loads(req.text)
            list_of_results.append(result)
            """for k in range(0, 2):
                list_of_results.append(result[k]["weather"])"""
        return list_of_results
