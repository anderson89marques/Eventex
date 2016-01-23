from django.test import TestCase
from eventx.core.models import Speaker
from django.shortcuts import resolve_url as r

class SpeakerModelTest(TestCase):
    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            website='http://hbn.link/hopper-site',
            photo='http://hbn.link/hopper-pic',
            description='Programadora e almirante.'
        )

    def test_create(self):
        self.assertTrue(Speaker.objects.exists())

    def test_description_can_be_blank(self):
        #pegando o campo description
        field = Speaker._meta.get_field('description')
        self.assertTrue(field.blank)

    def test_website_can_be_blank(self):
        #pegando o campo website
        field = Speaker._meta.get_field('website')
        self.assertTrue(field.blank)

    def test_str(self):
        self.assertEqual("Grace Hopper", str(self.speaker))

    def test_get_absolute(self):
        url = r('speaker_detail', slug=self.speaker.slug)
        self.assertEqual(url, self.speaker.get_absolute_url())