from django.urls import path
from .views import *

urlpatterns = [
    path('etape/',etape, name="etape"),
    path('fraisadmi/', frais, name='fraisadmi'),
]
