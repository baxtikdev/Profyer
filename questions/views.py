from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .models import Page, Category, UserAnswer
from .paginator import CustomPagination
from .serializer import ServiceSerializer, PageSerializer, CategorySerializer, UserAnswerSerializer
from users.models import Service
from .tasks import add_ans


class ServiceAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class PageAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class QuestionAPIView(mixins.ListModelMixin, GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination


class UserAnswerAPIView(mixins.CreateModelMixin, GenericViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_ans.delay(serializer.data)
        return Response(status=status.HTTP_200_OK)
