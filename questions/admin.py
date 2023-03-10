from django.contrib import admin
from parler.admin import TranslatableAdmin

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
            'fields': ['category', 'text', 'base'],
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
admin.site.register(UserAnswer)
