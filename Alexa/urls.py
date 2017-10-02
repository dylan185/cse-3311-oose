from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from AlexaApp.views import HomePageView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', auth_views.login, {'template_name': 'login.html'}, name='login_url'),
    url(r'^logout/', auth_views.logout, {'template_name': '/login/'},name='logout_url'),
    url(r'^home/', HomePageView.as_view(), name='home_page_url'),
]