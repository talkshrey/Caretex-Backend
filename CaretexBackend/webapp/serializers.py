from django.contrib.auth.backends import UserModel
from rest_framework import  serializers
from rest_framework.authtoken.models import Token
from . import models
from django.contrib.auth.models import User


class StaffList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# for api of products sold by auth seller
class ProductList(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

#  for api of authorised buyers
class UserList(serializers.ModelSerializer):
    class Meta:
        model = models.Buyer
        fields = '__all__'

# for api of products sold by third party seller
class OutsiderList(serializers.ModelSerializer):
    class Meta:
        model = models.Outsider
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    