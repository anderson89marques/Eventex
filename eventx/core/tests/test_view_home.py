from django.test import TestCase
from django.shortcuts import resolve_url as r


class HomeTest(TestCase):
    fixtures = ['keynotes.json']

    def setUp(self):
        self.response = self.client.get(r('home'))

    def test_get(self):
        """ GET / must return status code 200 """
        self.assertEqual(200, self.response.status_code)

    def test_templateUsed(self):
        """ Must use index.html """
        self.assertTemplateUsed(self.response, 'index.html')

    def test_subscrition_link(self):
        expected = 'href="{}"'.format(r('subscription:new'))
        self.assertContains(self.response, expected)

    def test_speakers(self):
        """must show keynotes speakers"""
        content = ['href="{}"'.format(r('speaker_detail', slug='grace-hopper')),
                   "Grace Hopper",
                   "http://hbn.link/hopper-pic",
                   'href="{}"'.format(r('speaker_detail', slug='alan-turing')),
                   "Alan Turing",
                   "http://hbn.link/turing-pic"]
        for expected in content:
            with self.subTest():
                self.assertContains(self.response, expected)

    def test_speaker_link(self):
        expected = 'href="{}#speakers"'.format(r('home'))
        self.assertContains(self.response, expected)