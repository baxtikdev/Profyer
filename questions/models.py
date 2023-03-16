from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _

from users.models import UserVote, UserType


class Page(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name of Page"), max_length=50)
    )

    def __str__(self):
        return self.name


class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name of Category"), max_length=50)
    )

    def __str__(self):
        return self.name


class QuestionType(models.TextChoices):
    CHOICE = 'CHOICE', _('CHOICE')
    CHECKBOX = 'CHECKBOX', _('CHECKBOX')
    NUMBER = 'NUMBER', _('NUMBER')
    AGE = 'AGE', _('AGE')


class Question(TranslatableModel):

    base = models.IntegerField(default=UserType.CLIENT, choices=UserType.choices)
    translations = TranslatedFields(
        text=models.TextField(_("Question text")),
    )
    category = models.ForeignKey(Category, related_name='category_question', on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=10, default=QuestionType.CHOICE, choices=QuestionType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:20] + ' ' + str(self.base)


class Option(TranslatableModel):
    question = models.ForeignKey(Question, related_name='question_option', on_delete=models.CASCADE)
    translations = TranslatedFields(
        text=models.TextField(_("Option text"))
    )

    def __str__(self):
        return self.text[:20]


class UserAnswer(models.Model):
    user = models.ForeignKey(UserVote, related_name='user_vote', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='user_question', on_delete=models.CASCADE)
    answer = models.ManyToManyField(Option, related_name='user_option')

    def __str__(self):
        return str(self.user.id) + ' ' + self.user.email
