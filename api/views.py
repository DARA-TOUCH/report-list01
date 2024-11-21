from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from rest_framework.response import Response
from django.shortcuts import render


class CreateUserView(generics.CreateAPIView, TemplateView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    template_name = 'register.html'
    permission_classes = [AllowAny]


class LoginTemplateView(TemplateView):
    template_name = 'login.html'
    permission_classes = [AllowAny]



class HomePageView(TemplateView):
    template_name = 'base.html'
    permission_classes = [IsAuthenticated]


def test(request):
    return render(request, 'test.html')