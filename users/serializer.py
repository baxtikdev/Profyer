from rest_framework import serializers

from questions.translations import TranslatedSerializerMixin
from users.models import UserVote, Language, Country
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=255)


class UserVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserVote
        fields = ['id', 'first_name', 'last_name', 'email', 'language', 'services', 'type']


class NumberUserVoteSerializer(serializers.Serializer):
    number = serializers.IntegerField(max_value=10, min_value=1, required=True)


class AgeUserVoteSerializer(serializers.Serializer):
    age = serializers.IntegerField(max_value=100, min_value=5, required=True)


class LanguageSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Language)

    class Meta:
        model = Language
        fields = '__all__'


class CountrySerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Country)

    class Meta:
        model = Country
        fields = '__all__'
