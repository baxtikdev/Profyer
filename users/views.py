from rest_framework import generics, mixins, status
from rest_framework.viewsets import GenericViewSet
from .serializer import UserVoteSerializer, NumberUserVoteSerializer, AgeUserVoteSerializer, LanguageSerializer
from rest_framework.response import Response
from .models import UserVote, Language
from .tasks import partial_update


class LanguageAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class CreateUserAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = UserVoteSerializer


class NumberUserVoteAPIView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = NumberUserVoteSerializer
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partial_update.delay(kwargs.get('pk'), serializer.data.get('number'), 'number')
        return Response(status=status.HTTP_200_OK)


class AgeUserVoteAPIView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = AgeUserVoteSerializer
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partial_update.delay(kwargs.get('pk'), serializer.data.get('age'), 'age')
        return Response(status=status.HTTP_200_OK)
