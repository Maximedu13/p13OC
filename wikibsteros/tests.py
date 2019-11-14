from django.test import TestCase

# Create your tests here.
class Page(TestCase):
    def test_wrong_uri_returns_404(self):
        response = self.client.get('something/really/weird/')
        self.assertEqual(response.status_code, 404)
        
class Character(TestCase):
    def setUp(self):
        pass

    def test_animals_can_speak(self):
        pass