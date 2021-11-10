from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from rest_framework import generics, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import HttpResponse, response
from . import serializers, models, forms
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.
def index(request):
    return HttpResponse("This is Home Page")

#Register User
def signup(request):
    register = forms.CreateUser()
    if request.method == 'POST':
        forms.CreateUser(request.POST)
        if register.is_valid():
            register.save()
            login(request, forms)
            subject = 'Welcome to Caretex'
            message = f'Hi {forms.username}, Thank you for registering in Caretex.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [forms.email, ]
            send_mail( subject, message, email_from, recipient_list )
            return response(register)
        else:
            return HttpResponse('form not filled')
    return HttpResponse('Not valid')

# Login User
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")
        
        else:
            #login page
            return render(request, '/')
    #login page
    return render(request, '/')

# Logout User
def logoutUser(request):
    #redirect to login page
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, '/')

def about(request):
    return HttpResponse("This is About Page")

def contact(request):
    return HttpResponse("This is Contact Page")

def services(request):
    return HttpResponse("This is Services Page")


class Staff(generics.ListAPIView):

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user)
    
    serializer_class = serializers.StaffList
    permission_classes = [IsAuthenticated]

# generic API view for products sold by authorised seller
class Products(generics.ListAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductList
    permission_classes = [IsAuthenticated]

# mixin views for outsider models
class ThirdPartyList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = models.Outsider.objects.all()
    serializer_class = serializers.OutsiderList
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class based views
class CustomAuthToken(ObtainAuthToken):

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid()
        user = serializer.validated_data()
        token = Token.objects.get_or_create(user=user)
        return Response(token)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created, **kwargs):
    Token.objects.get_or_create(user=instance)
    print('Token created')

@receiver(post_delete, sender=User)
def delete_auth_token(sender, instance, **kwargs):   
    print('Token deleted')


class Tokens(generics.ListAPIView):
    queryset = Token.objects.all()
    serializer_class = serializers.TokenSerializer
    permission_classes = [IsAuthenticated]

class SignUpList(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]