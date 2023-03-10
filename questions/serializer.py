from rest_framework import serializers
from .models import Page, Category, Question, Option, UserAnswer
from users.models import Service
from .translations import TranslatedSerializerMixin
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField


class PageSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Page)

    class Meta:
        model = Page
        fields = '__all__'


class CategorySerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Category)

    class Meta:
        model = Category
        fields = '__all__'


class ServiceSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Service)

    class Meta:
        model = Service
        fields = '__all__'


class OptionSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Option)

    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    category = CategorySerializer(read_only=True, many=False)
    translations = TranslatedFieldsField(shared_model=Question)

    class Meta:
        model = Question
        exclude = ['created_at']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['options'] = OptionSerializer(instance.question_option.all(), many=True).data
        return response


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
