from django.db import models
from django.shortcuts import resolve_url as r
from eventx.core.managers import KindQuerySet, PeriodManager


class Speaker(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    website = models.URLField('website', blank=True)
    photo = models.URLField('foto')
    description = models.TextField('descrição', blank=True)

    class Meta:
        verbose_name = 'palestrante'
        verbose_name_plural = 'palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)


class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'

    KINDS = (
        (EMAIL, 'email'),
        (PHONE, 'telefone')
    )

    speaker = models.ForeignKey('Speaker', verbose_name="palestrante")
    kind = models.CharField('tipo', max_length=1, choices=KINDS)
    value = models.CharField('valor', max_length=255)

    #criando um manager a partir do QuerySet
    objects = KindQuerySet.as_manager()

    class Meta:
        verbose_name = 'contato'
        verbose_name_plural = 'contatos'

    def __str__(self):
        return self.value


class Activity(models.Model):
    title = models.CharField("título", max_length=200)
    start = models.TimeField("início", blank=True, null=True)
    description = models.TextField("descrição", blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name="palestrantes", blank=True)

    objects = PeriodManager()

    class Meta:
        abstract = True #indicando que essa classe é abstrata
        verbose_name="Palestra"
        verbose_name_plural="Palestras"

    def __str__(self):
        return self.title


class Talk(Activity):
    pass


class Course(Activity):
    slots = models.IntegerField()

    class Meta:
        verbose_name_plural="cursos"
        verbose_name="curso"