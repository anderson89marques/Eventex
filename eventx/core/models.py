from django.db import models
from django.shortcuts import resolve_url as r

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


class Talk(models.Model):
    title = models.CharField("título", max_length=200)
    start = models.TimeField("início", blank=True, null=True)
    description = models.TextField("descrição", blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name="palestrantes", blank=True)

    class Meta:
        verbose_name="Palestra"
        verbose_name_plural="Palestras"

    def __str__(self):
        return self.title