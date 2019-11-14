"""Create your models here."""
from django.db import models
from django.contrib.auth.models import User

DEFAULT_CONTENT = 'This section is empty, \
    you can help to improve our community by adding to it.'

# Create your models here.
class Character(models.Model):
    """Character class"""
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=30)
    culture = models.CharField(max_length=200)
    titles = models.CharField(max_length=1000)
    origin = models.CharField(max_length=200, default='Unknown')
    siblings = models.CharField(max_length=1000, default='Unknown')
    spouse = models.CharField(max_length=200, default='Unknown')
    lovers = models.CharField(max_length=200, default=None)
    religion = models.CharField(max_length=200, default='Unknown')
    allegiances = models.CharField(max_length=200)
    image = models.ImageField(default='', max_length=1000)
    alive = models.BooleanField(default=None)
    died = models.CharField(max_length=200)
    father = models.CharField(max_length=200)
    mother = models.CharField(max_length=200, default='')
    house = models.CharField(max_length=200, default=None)
    playedBy = models.CharField(max_length=200)
    location = models.CharField(max_length=300, default='Unknown')
    age = models.IntegerField(default=None)
    note = models.FloatField(default=1.00)
    s_1 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_2 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_3 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_4 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_5 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_6 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_7 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_8 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    s_9 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    book_1 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    book_2 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    book_3 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    book_4 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)
    book_5 = models.CharField(max_length=10**6, default=DEFAULT_CONTENT)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Article class"""
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10**6)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.content

class Houses(models.Model):
    """Houses class"""
    name = models.CharField(max_length=200)
    """def __str__(self):
        return self.name"""

class City(models.Model):
    """Cities class"""
    name = models.CharField(max_length=200, default='None')
    rulers = models.CharField(max_length=200, default='None')
    religion = models.CharField(max_length=200, default='None')
    location = models.CharField(max_length=200, default='None')
    founder = models.CharField(max_length=200, default='None')
    population = models.IntegerField(default=0)
    type = models.CharField(max_length=200, default='None')
    image = models.ImageField(default='', max_length=1000)
    def __str__(self):
        return self.name

class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

class PostACommentCity(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    def __str__(self):
        return self.message

class PostACommentCharacter(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    def __str__(self):
        return self.message

class PostACommentArticle(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    def __str__(self):
        return self.message

class UserChoices(models.Model):
    """caracteristics of the users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    chosen_allegiance = models.CharField(max_length=200)
    chosen_region = models.CharField(max_length=200)

class VotesCharacters(models.Model):
    """ votes of the users """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    note = models.FloatField(default=1.00)
