from django.conf import settings
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from questions.views import QuestionAPIView, UserAnswerAPIView, ServiceAPIView, PageAPIView, GetAnswerAPIView
from users.views import NumberUserVoteAPIView, AgeUserVoteAPIView, CreateUserAPIView, LanguageAPIView, CountryAPIView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("user", CreateUserAPIView)
# router.register("user-vote", NumberUserVoteAPIView)
# router.register("user-age", AgeUserVoteAPIView)
router.register("services", ServiceAPIView)
router.register("languages", LanguageAPIView)
router.register("countries", CountryAPIView)
router.register("questions", PageAPIView)
# router.register("user-answer", UserAnswerAPIView)
router.register("answers", GetAnswerAPIView)

app_name = "api"
urlpatterns = router.urls

# TODO: USERS urls
urlpatterns += [
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
