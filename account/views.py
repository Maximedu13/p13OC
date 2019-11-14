import emoji
import urllib.request
import json
from wikibsteros.models import UserChoices, VotesCharacters
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
from wikibsteros.views import return_char

def index(request):
    message = "Salut tout le monde !"
    return HttpResponse(message)

def profile(request):
    """user profile view"""
    template = loader.get_template('profile.html')
    current_user = request.user
    profile_choice = UserChoices.objects.filter(user=current_user.id)
    profile_votes = VotesCharacters.objects.filter(user_id=current_user.id)
    stars = emoji.emojize(':star:', use_aliases=True)
    notes = {}
    for j in profile_votes:
        notes[j.character.id] = int(j.note) * stars
    if profile_choice:
        for p in profile_choice:
            chosen_allegiance = p.chosen_allegiance
            chosen_region = p.chosen_region
    elif not profile_choice.exists():
        chosen_allegiance = None
        chosen_region = None
    else:
        pass
    try:
        with urllib.request.urlopen("https://geoip-db.com/json") as url:
            data = json.loads(url.read().decode())
            city = data['city']
            country = data['country_name']
            state = data['state']
    except:
        result = " adresse introuvable. "
    the_flag = emoji.emojize(':' +  country + ':', use_aliases=True)

    if not current_user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    message = {
        'user' : current_user, 'city' : city, 'country' : country, 'state' : state,
        'the_flag' : the_flag, 'chosen_allegiance' : chosen_allegiance,
        'chosen_region' : chosen_region, 'notes' : notes, 'stars' : stars
    }
    return HttpResponse(template.render(message, request=request))
