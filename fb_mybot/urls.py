# mybot/fb_mybot/urls.py
from django.conf.urls import include, url
from .views import MyBotView
urlpatterns = [url(r'^2574a353fbbe79f772a98bc3a101a2783d3fa754f36e94ef5d/?$', MyBotView.as_view())]