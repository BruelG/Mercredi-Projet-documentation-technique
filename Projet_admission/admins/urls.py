from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboard, detail_demande,login
urlpatterns = [
    path('admin_admission/',login,name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('demande/<int:demande_id>/', detail_demande, name='detail_demande'),
]
# Ajouter ces lignes à la fin du fichier pour servir les fichiers médias en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)