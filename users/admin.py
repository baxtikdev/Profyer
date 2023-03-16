from django.contrib import admin
from parler.admin import TranslatableAdmin

from .models import Service, UserVote, Language
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.unregister(Group)


class ServiceAdmin(TranslatableAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
    )


admin.site.register(Service, ServiceAdmin)


class LanguageAdmin(TranslatableAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',),
        }),
    )


admin.site.register(Language, LanguageAdmin)
admin.site.register(UserVote)


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)

    def save_model(self, request, obj, form, change):
        if len(str(obj.password)) < 30:
            obj.set_password(obj.password)
        super(User, self).save_model(request, obj, form, change)
