from django.urls import path
from .views import CalculatorView

app_name = 'java'

urlpatterns = [
    path('calculator/', CalculatorView.as_view(), name='calculator'),
]