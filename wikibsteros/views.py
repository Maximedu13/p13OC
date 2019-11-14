"""views of the app wikibsteros"""
import os
import random
import calendar
import datetime
import json
import pytz
import urllib
import online_users.models
from django.conf import settings
from .other_functions import situation_in_the_crowns, choose_a_region, \
battle_init, battle_cards, get_cards, fight, random_quote_maggy
from .database import InsertObjects, Article, WeatherObjects
from .constants import SECOND_ARTICLE_RESUME_EN
from django.http import HttpResponse
from .forms import LoginForm, RegisterForm, ContactForm, ChatRoomForm, ClairvoyanceForm
from .models import Character, Houses, Chat, City, PostACommentCity, UserChoices, \
PostACommentCharacter, UserChoices, PostACommentArticle, VotesCharacters
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.template import loader
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.translation import pgettext
from django.utils import translation
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext_lazy as __
from django.template.defaulttags import register
from django.template.defaultfilters import register
from django.http import JsonResponse, HttpResponseRedirect
from django import template

@register.filter
def index(List, i):
    return List[int(i)]

@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None

def set_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'GET':
        lang_code = request.GET.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            translation.activate(lang_code)
    return response


def get_hours(loc, zone):
    """ cities hours """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', \
    'September', 'October', 'November', 'December']
    got_loc = datetime.datetime.now(pytz.timezone(zone)) # you could pass `timezone` object here
    my_date = got_loc.today()
    fmt = '%I %M %S %p'
    result = loc, calendar.day_name[my_date.weekday()] + ',', got_loc.day, \
    months[got_loc.month - 1], str(got_loc.year), got_loc.strftime(fmt)
    return result

def set_hours():
    pyk = get_hours(_('Pyk, Casterly Rock, Oldtown'), 'Brazil/DeNoronha')
    sunspear = get_hours(_('Sunspear, Dragonstone, Storm‘s End'), 'Europe/Madrid')
    highgarden = get_hours(_('Highgarden, Riverrun, The Twins, Winterfell'), 'Etc/GMT+1')
    kings_landings = get_hours(_('King‘s Landings, The Eyrie, Castleblack'), 'Etc/GMT-1')
    tyrosh = get_hours('Tyrosh', 'Europe/Bucharest')
    hours_lefts = [pyk, highgarden, kings_landings, sunspear, tyrosh]
    pentos = get_hours('Pentos, Myr, Braavos, Lys', 'Europe/Bucharest')
    lorath = get_hours('Lorath, Norvos', 'Europe/Samara')
    volantis = get_hours('Volantis', 'Asia/Omsk')
    yunkai = get_hours('Yunkaï, Meeren, Astapor', 'Asia/Tokyo')
    qarth = get_hours('Qarth', 'Pacific/Fiji')
    hours_right = [pentos, lorath, volantis, yunkai, qarth]
    return hours_lefts, hours_right

def get_online_users():
    """display all online users"""
    user_activity_objects = online_users.models.OnlineUserActivity.get_user_activities\
    (datetime.timedelta(minutes=1))
    number_of_active_users = user_activity_objects.count()
    list_of_onlines = []
    for act in user_activity_objects:
        list_of_onlines.append(User.objects.get(pk=act.user_id))
    print(list_of_onlines)
    template = loader.get_template('footer.html')
    return list_of_onlines, number_of_active_users

def get_the_name_from_the_user_id(this_id):
    char = User.objects.filter(id=this_id)
    for this_char in char:
        return this_char.username

@register.simple_tag
def get_the_id_from_the_character(this_name):
    char = Character.objects.filter(name=this_name)
    for this_char in char:
        return this_char.id

@register.simple_tag
def get_the_id_from_the_house(this_name):
    house = Houses.objects.filter(name=this_name)
    for this_house in house:
        return this_house.id

def get_the_picture_from_the_char_id(id):
    char = Character.objects.filter(id=id)
    for this_char in char:
        return this_char.image

@register.simple_tag
def get_the_location_from_the_char_id(id):
    char = Character.objects.filter(id=str(id))
    for this_char in char:
        return _(this_char.location)

@register.simple_tag
def get_the_id_from_the_city_name(name):
    city = City.objects.filter(name=name)
    for this_city in city:
        return str(this_city.id)

@register.simple_tag
def loc_pandas_char(the_list, a_a, b_b):
    return the_list.loc[a_a, b_b]

@register.simple_tag
def random_item_in_list(the_list):
    return random.choice(the_list)

def get_current_lang():
    """ get the langage of the web page : fr or en or cl"""
    return translation.get_language()

@register.simple_tag
def translate(text):
    try:    
        return _(text)
    except:
        print("exception")

def index(request):
    """index page"""
    # cities hours recovery
    hours_lefts, hours_right = set_hours()
    # call the function crown situation
    days_passed, names_sovereings, names_houses, names_regions, names_images, \
    names_landscapes = situation_in_the_crowns()
    # insert objects in database
    InsertObjects.insert_houses()
    InsertObjects.insert_articles()
    InsertObjects.insert_users()
    InsertObjects.insert_cities()
    InsertObjects.insert_characters()
    InsertObjects.update_char_from_database()
    InsertObjects.update_city_from_database()
    
    #InsertObjects.get_id_char()
    three_recent_articles = Article.objects.order_by('-date')[:3]
    articles = Article.objects.all()
    choose_a_region()
    #dict_users()
    # Get the number of online people django (last activity max = one minute)
    list_of_onlines, number_of_active_users = get_online_users()

    if request.method == 'POST':
        # A form bound to the POST data
        form_1 = LoginForm(request.POST)
        form_2 = RegisterForm(request.POST)
        form_3 = ContactForm(request.POST)
        form_4 = ChatRoomForm(request.POST)
        # All validation rules pass
        if form_1.is_valid():
            # Process the data in form.cleaned_data
            user = form_1.cleaned_data['user']
            mdp = form_1.cleaned_data['mdp']
            user = authenticate(username=user, password=mdp)
            login(request, user)
            messages.success(request, 'Vous avez été connecté.')
            request.session.set_expiry(900)
            return redirect('index')
        if form_2.is_valid():
            mail = request.POST.get('email')
            user_name = request.POST.get('user_name')
            password = request.POST.get('password')
            allegiance = request.POST.get('field_1')
            region = request.POST.get('field_2')
            email = form_2.cleaned_data['email']
            username = form_2.cleaned_data['user_name']
            raw_password = form_2.cleaned_data['password']
            recaptcha_response = request.POST.get('g-recaptcha-response')
            #---- captcha -----#
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            if recaptcha_response:
                try:
                    User.objects.create_user(username, mail, raw_password)
                    UserChoices.objects.create(chosen_allegiance=allegiance, \
                    chosen_region=region, user_id=User.objects.all().count()+2)
                    messages.success(request, _("Your account has been successfully created. You can now log in."))
                    return redirect('index')
                except:
                    messages.error(request, _("Oops. It seems that something gets wrongs."))
                    return redirect('index')
            else:
                messages.error(request, _("It seems that the captcha has not been validated."))
                return redirect('index')
        if form_3.is_valid():
            subject = form_3.cleaned_data['subject']
            from_email = form_3.cleaned_data['from_email']
            message = form_3.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['websteros@yahoo.com'])
                messages.success(request, _('Your email has been sent.'))
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('index')
        if form_4.is_valid():
            chat = form_4.cleaned_data['chat']
            current_user = request.user
            user = User.objects.get(id=current_user.id)
            print(chat)
            #staffprofile.user = user
            Chat.objects.create(message=chat, user_id=user.id)
            #return JsonResponse({'msg': chat})

    else:
        form_1 = LoginForm() # An unbound form
        form_2 = RegisterForm()
        form_3 = ContactForm()
        form_4 = ChatRoomForm()

    all_chat_messages = Chat.objects.all()
    print(get_current_lang())

    return render(request, 'index.html', {
        'form_1': form_1, 'form_2': form_2, 'form_3': form_3, 'form_4': form_4,
        'names_sovereings' : names_sovereings, 'names_houses' : names_houses,
        'range_one': range(1, 5), 'three_recent_articles': three_recent_articles,
        'articles': articles, 'hours_left': hours_lefts,
        'hours_right': hours_right, 'days_passed': days_passed, 'list_of_onlines': list_of_onlines,
        'number_of_active_users': number_of_active_users, 'all_chat_messages' : all_chat_messages,
        'names_images' : names_images, 'names_landscapes' : names_landscapes,
        'range_two': range(5, 9), 'names_regions' : names_regions,
        'range_char' : range(0, 2)
    })

def wikibsteros(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render(request=request))


def add_a_vote_character(request, char_id):
    """ the user can rate a character from 1 to 5. """
    current_user = request.user
    this_id = Character.objects.filter(id=char_id)
    for s in this_id:
        this_note = float(s.note)
    list_of_notes = []
    list_of_notes.append(this_note)
    if request.method == 'POST':
        the_note = request.POST.get('rating')
        if VotesCharacters.objects.filter(character_id=char_id, user_id=current_user.id):
            messages.error(request, _('Sorry, but you‘ve already voted for this character. \
            Votes are limited to one character per account.'))
        else:
            list_of_notes.append(float(the_note))
            update_note = (list_of_notes[0] * 99 + list_of_notes[1]) / 100
            Character.objects.filter(id=char_id).update(note=update_note)
            VotesCharacters.objects.get_or_create(character_id=char_id, user_id=current_user.id,
                                                  note=float(the_note))
        return HttpResponseRedirect(reverse('wikibsteros:character', args=(char_id,)))

def wikibsteros_search(request):
    """ the user can search in encyclopedia """
    # GET THE CURRENT LANGUAGE
    lang = get_current_lang()
    if request.GET.get('query') is not None:
        query = request.GET.get('query')
        print(query)
        try:
            character_search = get_the_id_from_the_character(query)
            city_search = get_the_id_from_the_city_name(query)
            house_search = get_the_id_from_the_house(query)
            # SUCCESS
            if character_search:
                url = '{lang}/wikibsteros/character/{query}'.format(lang=lang, query=character_search)
                return HttpResponseRedirect('/'+url)
            elif city_search:
                url = '{lang}/wikibsteros/city/{query}'.format(lang=lang, query=city_search)
                return HttpResponseRedirect('/'+url)
            elif house_search:
                url = '{lang}/wikibsteros/house/{query}'.format(lang=lang, query=house_search)
                return HttpResponseRedirect('/'+url)
            # FAIL
            else:
                messages.error(request, _('Sorry, but it seems to be an invalid request'))
                return redirect('index')
        except:
            return redirect('index')
    else:
        return redirect('index')


def universe(request):
    template = loader.get_template('universe.html')
    characters, cities = Character.objects.order_by('-note')[:3], City.objects.order_by('-population')[:3]
    print(characters)
    print(cities)
    the_path = request.get_full_path()
    the_path = the_path.split('/')
    the_path = the_path[2:]
    print('THIS PATH', the_path)
    universe = {
        'characters' : characters,
        'cities' : cities,
        'the_path' : the_path
    }
    return HttpResponse(template.render(universe, request=request))

def maggy(request):
    """ Maggy page"""
    template = loader.get_template('maggy.html')
    list_of_onlines, number_of_active_users = get_online_users()
    if request.method == 'POST':
        quote, autor = random_quote_maggy()
        # A form bound to the POST data
        form_voyance = ClairvoyanceForm(request.POST)
        gender = request.POST.get('field_1')
        char = request.POST.get('character')
        if form_voyance.is_valid and char and gender:
            return HttpResponse('<blockquote class="blockquote text-center">' + \
                    '<p class="mb-0">' + quote + '</p>' + \
                    '<footer class="blockquote-footer">' + autor + '</footer>' + \
                    '</blockquote>')
        else:
            redirect("")
    else:
        # An unbound form
        form_voyance = ClairvoyanceForm()
    message = {
        'form_voyance' : form_voyance,
        'list_of_onlines' : list_of_onlines, 'number_of_active_users' : number_of_active_users
    }
    return HttpResponse(template.render(message, request=request))

def autocomplete(request):
    """autocomplete ajax"""
    if request.is_ajax():
        query_autocomplete = request.GET.get('term', '')
        # THE USER CAN SEARCH FOR CHARACTERS, HOUSES, AND CITIES
        characters = Character.objects.filter(name__icontains=query_autocomplete).\
        order_by('id')[:10]
        houses = Houses.objects.filter(name__icontains=query_autocomplete).\
        order_by('id')[:10]
        cities = City.objects.filter(name__icontains=query_autocomplete).\
        order_by('id')[:10]
        results = []
        product_dict = {}
        # FILL THE DICTIONNARY
        for char in characters:
            product_dict = char.name
            results.append(product_dict)
        for house in houses:
            product_dict = house.name
            results.append(product_dict)
        for city in cities:
            product_dict = city.name
            results.append(product_dict)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, 'application/json')

# Create your views here.
def log_out(request):
    """method to log out the user"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('index')

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def battle(request):
    template = loader.get_template('battle.html')
    dirs, lang_web, list_characters, cards = get_cards()
    files = {
        'dirs': dirs,
        'lang_web' : lang_web,
        'list_characters': list_characters,
        'cards' : cards
    }
    return HttpResponse(template.render(files, request=request))


def battle_result(request):
    template = loader.get_template('battle_result.html')
    family = battle_init()
    dirs, lang_web, list_characters, cards = get_cards()
    selected = request.POST.getlist('checkbox')
    hp_night_king = 999
    if len(selected) != 4:
        messages.warning(request, _('Sorry, but you need to select four cards. Try again.'))
        return redirect('wikibsteros:battle')
    else:
        selected, random_attack, iterations, status_game, char_1_hp_list, \
        char_2_hp_list, char_3_hp_list, char_4_hp_list, hp_night_king_list = fight(selected, family)
        char_1_hp_list = [(i > 0) * i for i in char_1_hp_list]
        char_2_hp_list = [(i > 0) * i for i in char_2_hp_list]
        char_3_hp_list = [(i > 0) * i for i in char_3_hp_list]
        char_4_hp_list = [(i > 0) * i for i in char_4_hp_list]
        hp_night_king_list = [(i > 0) * i for i in hp_night_king_list]
        results = {
            'selected' : selected, 'lang_web' : lang_web, 'cards' : cards,
            'range_one' : range(0, 2), 'range_two' : range(2, iterations),
            'range' : range(0, len(selected)), 'family' : family,
            'random_attack' : random_attack, 'hp_night_king' : hp_night_king,
            'iterations' : range(0, iterations), 'status_game' : status_game,
            'char_1_hp_list' : char_1_hp_list, 'char_2_hp_list' : char_2_hp_list,
            'char_3_hp_list' : char_3_hp_list, 'char_4_hp_list' : char_4_hp_list,
            'hp_night_king_list' : hp_night_king_list
        }
        return HttpResponse(template.render(results, request=request))

def test_i18n(request):
    nb_chats = 2
    couleur = "blanc"
    chaine = _("J'ai un %(animal)s %(col)s.") % {'animal': 'chat', 'col': couleur}
    infos = ungettext(
        "… et selon mes informations, vous avez %(nb)s chat %(col)s !",
        "… et selon mes informations, vous avez %(nb)s chats %(col)ss !",
        nb_chats) % {'nb': nb_chats, 'col': couleur}
    verbe = pgettext("verbe 'avoir'", "as")
    valeur = pgettext("carte de jeu", "as")
    carte = _("%(suj)s %(ver)s : %(val)s %(col)s") % {
        "suj": _("tu"),
        "ver": verbe,
        "val": valeur,
        "col": _("de trèfle")}
    translation.activate('en')
    jac = _("Bonjour les nouveaux !")
    print(jac)
    return render(request, 'test_i18n.html', locals())

def weather(request):
    """weather view"""
    template = loader.get_template('weather.html')
    forecast = WeatherObjects.call_api()
    dict = WeatherObjects.create_dict()
    keys = []
    for key in dict.items():
        keys.append(key[0])
    list_of_temp, list_of_weathers, list_of_pressures, list_of_humidities, list_of_winds = \
    [], [], [], [], []
    for i in range(0, len(forecast)):
        list_of_weathers.append(forecast[i]["weather"][0]["main"])
        list_of_temp.append(round(forecast[i]["main"]["temp"] -273.15))
        list_of_pressures.append(forecast[i]["main"]["pressure"])
        list_of_humidities.append(forecast[i]["main"]["humidity"])
        list_of_winds.append(round(forecast[i]["wind"]["speed"] * 3.6))
    weather = {
        'range_one': range(12, 14), 'range_two': range(14, 17),
        'range_three' : range(17, 21), 'range_four' : range(21, 25),
        'range_five' : range(25, 29), 'dict': dict, 'keys' : keys,
        'list_of_temp' : list_of_temp, 'list_of_weathers' : list_of_weathers,
        'list_of_humidities' : list_of_humidities, 'list_of_pressures' : list_of_pressures,
        'list_of_winds' : list_of_winds
    }
    return HttpResponse(template.render(weather, request=request))

def character(request, id):
    """character details view"""
    template = loader.get_template('character.html')
    #print(get_the_id_from_the_city_name("Asshai"))
    this_character = Character.objects.get(pk=id)
    try:
        next = Character.objects.get(pk=int(id) + 1)
    except:
        next = None
    try:
        previous = Character.objects.get(pk=int(id) - 1)
    except:
        previous = None

    blank = "This section is empty,     you can help to improve our community by adding to it."
    if this_character.s_1 == this_character.s_2 == this_character.s_3 == \
    this_character.s_4 == this_character.s_5 == this_character.s_6 == \
    this_character.s_7 == this_character.s_8 == this_character.s_9 == blank:
        this_empty_section = True
    else:
        this_empty_section = False
    number_of_rows = Character.objects.all().count()
    books = ["A Game of Thrones", "A Clash of Kings", "A Storm of Swords",
             "A Feast for Crows", "A Dance with Dragons"]
    seasons = ['s_1', 's_1', 's_2', 's_3', 's_4', 's_5', 's_6', 's_7', 's_8', 's_8', 's_8']
    comments = PostACommentCharacter.objects.filter(character_id=id)
    number_of_comments = comments.count()

    message = {
        'this_character': this_character, 'books': books,
        'range_one': range(1, 9), 'range_two': range(0, 8),
        'seasons': seasons, 'previous' : previous, 'next' : next,
        'random_character': random.randint(1, number_of_rows),
        'comments' : comments, 'number_of_comments' : number_of_comments,
        'blank' : blank, 'this_empty_section': this_empty_section
    }

    return HttpResponse(template.render(message, request=request))

def house(request, id):
    """house details view"""
    template = loader.get_template('house.html')
    this_house = Houses.objects.get(pk=id)
    message = {
        'this_house': this_house
    }
    return HttpResponse(template.render(message, request=request))


def add_a_comment_city(request, city_id):
    """POST A COMMENT ON A CITY PAGE"""
    this_message = request.POST.get('message')
    current_user = request.user
    PostACommentCity.objects.get_or_create(message=this_message, \
    city_id=city_id, user_id=current_user.id)
    return HttpResponseRedirect(reverse('wikibsteros:city', args=(city_id,)))

def add_a_comment_character(request, character_id):
    """POST A COMMENT ON A CHARACTER PAGE"""
    this_message = request.POST.get('message')
    current_user = request.user
    PostACommentCharacter.objects.get_or_create(message=this_message, \
    character_id=character_id, user_id=current_user.id)
    return HttpResponseRedirect(reverse('wikibsteros:character', args=(character_id,)))

def add_a_comment_article(request, article_id):
    """POST A COMMENT ON A CHARACTER PAGE"""
    this_message = request.POST.get('message')
    current_user = request.user
    PostACommentArticle.objects.get_or_create(message=this_message, \
    article_id=article_id, user_id=current_user.id)
    return HttpResponseRedirect(reverse('wikibsteros:article', args=(article_id,)))

def city(request, id):
    """city details view"""
    template = loader.get_template('city.html')
    this_city = City.objects.get(pk=id)
    try:
        next = City.objects.get(pk=int(id) + 1)
    except:
        next = None
    try:
        previous = City.objects.get(pk=int(id) - 1)
    except:
        previous = None
    rank = list(City.objects.all().order_by('-population')).index(this_city)
    if rank == 0:
        exponent = "st"
    elif rank == 1:
        exponent = "nd"
    elif rank == 2:
        exponent = "rd"
    else:
        exponent = "th"
    rank = str(rank + 1)
    number_of_rows = City.objects.all().count()
    comments = PostACommentCity.objects.filter(city_id=id)
    number_of_comments = comments.count()
    print(number_of_comments)
    dict_users()
    message = {
        'this_city': this_city, 'previous' : previous, 'next' : next,
        'random_city': random.randint(1, number_of_rows),
        'comments' : comments, 'rank' : rank, "exponent" : exponent,
        'number_of_comments' : number_of_comments
    }
    
    return HttpResponse(template.render(message, request=request))


@register.simple_tag
def multiply_by_two(value):
    return float(value) * 2.0


@register.simple_tag
def call_method(obj, method_name, *args):
    method = getattr(obj, method_name)
    return method(*args)


def dict_users():
    print(User.objects.all())

@register.simple_tag
def return_char(char_id):
    return get_the_name_from_the_user_id(str(char_id))


@register.simple_tag
def return_image(char_id):
    return get_the_picture_from_the_char_id(str(char_id))

def articles(request):
    template = loader.get_template('articles.html')
    articles = Article.objects.all().order_by('-date')
    all_articles = {
        'articles': articles,
    }
    return HttpResponse(template.render(all_articles, request=request))


def article(request, id):
    """article details view"""
    template = loader.get_template('article.html')
    InsertObjects.insert_articles()
    this_article = Article.objects.get(pk=id)
    TITLE = this_article.title
    comments = PostACommentArticle.objects.filter(article_id=id)
    number_of_comments = comments.count()
    message = {
        'this_article': this_article,
        'TITLE' : _(TITLE), 'number_of_comments' : number_of_comments,
        'comments' : comments
    }
    
    return HttpResponse(template.render(message, request=request))

def random_page(request, id):
    print(Character.objects.get(pk=id))
    return HttpResponse(template.render(message, request=request))

register = template.Library()
