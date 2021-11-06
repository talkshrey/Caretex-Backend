from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # main pages
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('services', views.services, name="services"),

    # api views
    path('apiProd/', views.Products.as_view(), name="api"),
    path('apiParty', views.ThirdPartyList.as_view(), name="api2"),
    path('apiBuyer', views.CustomAuthToken.as_view(), name='api3'),
    path('apiStaff', views.Staff.as_view(), name='api4'),

    # auth views
    path('signup', views.signup, name="signup"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),

    path('tokenView', views.Tokens.as_view()),
    path('userview', views.SignUpList.as_view()),

]