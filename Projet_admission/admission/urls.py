from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('programme/', programme_view, name='programme'),   
    path('contact/', contact_view, name='contact'),
    path('propos/', propos_view, name='propos'),
    path('admission/', include("Utilisateurs.urls")),
    path('informations/', include("informations.urls")),
    path('demande_admission/', include('demande_admission.urls')),
    path('',include('admins.urls'))

]
