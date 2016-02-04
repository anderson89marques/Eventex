from django.test import TestCase
from eventx.core.managers import PeriodManager
from eventx.core.models import Talk


class TestModelTalk(TestCase):
    def setUp(self):
        self.talk = Talk.objects.create(
            title="Título da Palestra",
            start='10:00',
            description='Descrição da palestra.'
        )

    def test_create(self):
        self.assertTrue(Talk.objects.exists())

    def test_has_speakers(self):
        """talk has many speakers and vice-versa"""
        self.talk.speakers.create(
            name="Herinque Bastos",
            slug="henrique-bastos",
            website="http://henriquebastos.net"
        )

        self.assertEqual(1, self.talk.speakers.count())

    def test_description_blank(self):
        field = Talk._meta.get_field('description')
        self.assertTrue(field.blank)

    def test_start_blank(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.blank)

    def test_speakers_blank(self):
        field = Talk._meta.get_field('speakers')
        self.assertTrue(field.blank)

    def test_start_null(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.null)

    def test_str(self):
        self.assertEqual("Título da Palestra", str(self.talk))


class PeriodManageTest(TestCase):
    def setUp(self):
        Talk.objects.create(title="Morning Talk", start="11:59")
        Talk.objects.create(title="Afternoon Talk", start="12:00")

    def test_manager(self):
        self.assertIsInstance(Talk.objects, PeriodManager)

    def test_at_morning(self):
        qs = Talk.objects.at_morning()
        expected = ["Morning Talk"]
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)

    def test_at_afternoon(self):
        qs = Talk.objects.at_afternoon()
        expected = ["Afternoon Talk"]
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)