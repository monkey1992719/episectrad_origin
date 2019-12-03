from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^api/news-subscription$", views.NewsSubscriptionView.as_view(), name="news-subscription"),
]
