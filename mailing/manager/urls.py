from manager.views import auth
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from manager import views


router = routers.SimpleRouter()
router.register(r"clients", views.ClientViewSet, basename="client")
router.register(r"mailings", views.MailingViewSet, basename="mailing")


urlpatterns = [
    path("", include(router.urls)),
    path("mailings_statistics/",
         views.MailingGeneralStatistics.as_view()),
    path(
        "mailings_statistics/<int:pk>", views.MailingDetailStatistics.as_view()
    ),
    path("auth_page/", auth),
]

urlpatterns = format_suffix_patterns(urlpatterns)

