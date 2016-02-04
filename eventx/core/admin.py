from django.contrib import admin

# Register your models here.
from eventx.core.models import Speaker, Talk, Contact


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 1


class SpeakerModelAdmin(admin.ModelAdmin):
    inlines = [ContactInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name',  'photo_img', 'website_link', 'email', 'telefone']

    def website_link(self, obj):
        return '<a href={0}>{0}</a>'.format(obj.website)

    website_link.allow_tags = True
    website_link.short_description = 'website'

    def photo_img(self, obj):
        return '<img width="32px" src="{0}" />'.format(obj.photo)

    photo_img.allow_tags = True
    photo_img.short_description = 'foto'

    def email(self, obj):
        return obj.contact_set.emails().first()

    email.short_description = "e-mail"

    def telefone(self, obj):
        return obj.contact_set.phones().first()

    telefone.short_description = "telefone"

admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk)