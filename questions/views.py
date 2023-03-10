from rest_framework import generics, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Page, Category, Question, UserAnswer
from .serializer import ServiceSerializer, PageSerializer, CategorySerializer, QuestionSerializer, UserAnswerSerializer
from users.models import Service
from .tasks import add_ans


class ServiceAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]


class PageAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = [AllowAny]


class CategoryAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class QuestionAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class UserAnswerAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_ans.delay(serializer.data)
        return Response(status=status.HTTP_200_OK)
