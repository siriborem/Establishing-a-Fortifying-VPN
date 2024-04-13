from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.user_register, name='user_register'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('connect', views.connect_vpn, name='connect_vpn'),
    path('new', views.create_new_connection, name='create_new_connection'),
    path('disconnect', views.disconnect_vpn, name='disconnect_vpn'),
    path('open_browser/', views.open_browser, name='open_browser'),
    path('browse', views.browse, name='browse'),
]
