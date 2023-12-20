from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', base_demande_view, name='base_demande'),
    path('programme', etape_1_programme, name='etape_1'),
    path('information', etape_2_information, name='etape_2'),
    path('document', etape_3_document, name='etape_3'),
    path('payer', etape_4_payer, name='etape_4'),
    path('confrimer_payer', etape_5_confirmer, name='etape_5'),
    path('detail_confirmation', details_confirmation, name='details_confirmation')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)