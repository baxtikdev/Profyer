from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from .serializer import UserVoteSerializer, NumberUserVoteSerializer, AgeUserVoteSerializer, SexUserVoteSerializer
from rest_framework.response import Response
from .models import UserVote
from .tasks import partial_update


class ServiceAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = UserVoteSerializer
    permission_classes = [AllowAny]


class NumberUserVoteAPIView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = NumberUserVoteSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partial_update.delay(kwargs.get('pk'), serializer.data.get('number'), 'number')
        return Response(status=status.HTTP_200_OK)


class SexUserVoteAPIView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = SexUserVoteSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partial_update.delay(kwargs.get('pk'), serializer.data.get('sex'), 'sex')
        return Response(status=status.HTTP_200_OK)


class AgeUserVoteAPIView(mixins.UpdateModelMixin, GenericViewSet):
    queryset = UserVote.objects.all()
    serializer_class = AgeUserVoteSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        partial_update.delay(kwargs.get('pk'), serializer.data.get('age'), 'age')
        return Response(status=status.HTTP_200_OK)
