from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from questions.views import PageAPIView, CategoryAPIView, QuestionAPIView, UserAnswerAPIView
from users.views import ServiceAPIView, NumberUserVoteAPIView, SexUserVoteAPIView, AgeUserVoteAPIView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("user", ServiceAPIView)
router.register("user-vote", NumberUserVoteAPIView)
router.register("user-sex", SexUserVoteAPIView)
router.register("user-age", AgeUserVoteAPIView)
router.register("services", ServiceAPIView)
router.register("pages", PageAPIView)
router.register("categories", CategoryAPIView)
router.register("questions", QuestionAPIView)
router.register("user-answer", UserAnswerAPIView)

app_name = "api"
urlpatterns = router.urls

# TODO: USERS urls
urlpatterns += [
    # path('register/', RegisterAPIView.as_view(), name="register"),
    # path('verify/', VerifyCodeView.as_view(), name="verify"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    # path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('counts/', CountsAPIView.as_view(), name='counts')
]
