"""forms which manage the accounts"""
from django import forms
from langdetect import detect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from .other_functions import choose_a_region, choose_a_house, choose_a_character
from captcha.widgets import ReCaptchaV2Invisible, widgets

class LoginForm(forms.Form):
    """the form to login"""
    user = forms.CharField(max_length=100, widget=forms.TextInput(attrs=\
    {'placeholder': (_('Username')), 'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))
    mdp = forms.CharField(widget=forms.PasswordInput(attrs=\
    {'placeholder': (_('Password')), 'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))

class RegisterForm(forms.Form):
    """the form to create an account"""
    user_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs=\
    {'placeholder': (_('Username')), 'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs=\
    {'placeholder': 'E-mail', 'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs=\
    {'placeholder': (_('Password')), 'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))
    checkbox = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs=\
    {'style':'font-size:450%;'}))
    HOUSE_CHOICES = choose_a_house()
    field_1 = forms.ChoiceField(choices=HOUSE_CHOICES, label="",
                                required=True,
                                widget=forms.Select(attrs=\
                                {'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0 w-100'}))

    REGION_CHOICES = choose_a_region()
    field_2 = forms.ChoiceField(choices=REGION_CHOICES, label="",
                                required=True, widget=forms.Select(attrs=\
                                {'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0 w-100'}))

class ContactForm(forms.Form):
    """contact form"""
    from_email = forms.EmailField(widget=forms.EmailInput(attrs=\
    {'placeholder': (_('Your e-mail')),
     'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}),
                                  required=True)
    subject = forms.CharField(max_length=10**3, widget=forms.TextInput(attrs=\
    {'placeholder': (_('Subject')), 'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))
    message = forms.CharField(max_length=10**10, widget=forms.Textarea(attrs=\
    {'placeholder': (_('Your message')),
     'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0'}))

class ChatRoomForm(forms.Form):
    """chat room textarea"""
    chat = forms.CharField(max_length=10**10, widget=forms.Textarea(attrs=\
        {'placeholder': (_('Type your message')),
         'class': 'input-group-text d-flex bg-light rounded-0 w-100 text-lg-left'}))

class ClairvoyanceForm(forms.Form):
    """ Maggy form """
    GENDER_CHOICES = ((0, _('👨 CHOOSE A GENDER 👩')), ('Male', _('Male')), ('Female', _('Female')))
    
    field_1 = forms.ChoiceField(choices=GENDER_CHOICES, label="",
                                required=True,
                                widget=forms.Select(attrs=\
                                {'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0 w-100', \
                                'style' : 'text-align-last: center;'}))
    LIST_OF_CHARACTERS = choose_a_character()
    character = forms.ChoiceField(choices=LIST_OF_CHARACTERS, label="",
                                  required=True,
                                  widget=forms.Select(attrs=\
                                  {'class': 'form-control flex-fill mr-0 mr-sm-2 mb-3 mb-sm-0 w-100', \
                                   'style' : 'text-align-last: center;'}))
