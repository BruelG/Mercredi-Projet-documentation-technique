# ia_utils.py
import os
from django.core.files.storage import default_storage
from django.utils.html import format_html
from django.urls import reverse
from demande_admission import models as md 

def traiter_documents(demande):
    try:
        documents = md.Demander_Admission.Document_Fournir
        for doc in documents.all():
            print(doc)

    except Exception as e:
        print(f"Aucun document associé à cette demande. {e}")
