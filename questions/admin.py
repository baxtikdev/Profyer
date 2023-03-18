from django.contrib import admin
from parler.admin import TranslatableAdmin

from users.models import Country
from .models import Page, Category, Question, Option, UserAnswer


class PageAdmin(TranslatableAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ['name'],
        }),
    )


admin.site.register(Page, PageAdmin)


class CategoryAdmin(TranslatableAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ['name'],
        }),
    )


admin.site.register(Category, CategoryAdmin)


class QuestionAdmin(TranslatableAdmin):
    fieldsets = (
        (None, {
            'fields': ['category', 'type', 'text', 'base'],
        }),
    )


admin.site.register(Question, QuestionAdmin)


class OptionAdmin(TranslatableAdmin):
    fieldsets = (
        (None, {
            'fields': ['question', 'text'],
        }),
    )


admin.site.register(Option, OptionAdmin)


class CountryAdmin(TranslatableAdmin):
    fieldsets = (
        (None, {
            'fields': ['name'],
        }),
    )


admin.site.register(Country, CountryAdmin)
admin.site.register(UserAnswer)
