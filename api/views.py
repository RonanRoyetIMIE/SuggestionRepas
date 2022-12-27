from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from api.models import User

from django.contrib.auth.models import User
from api.serializers import UserSerializer, RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class RegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]