from asyncio import format_helpers
from django.utils.html import format_html
from django.http import FileResponse
from django.contrib import admin 
from django.urls import path, reverse
from .models import Programme,Information_Personnelle,Trimestre,ProgrammeTrimestre,Document_Fournir,Paiement,Coordonne_Bancaire,Demander_Admission

# Register your models here.
class ProgrammeTrimestreAdmin(admin.ModelAdmin):
    list_display = ('programme', 'trimestre') 
admin.site.register(ProgrammeTrimestre, ProgrammeTrimestreAdmin)
admin.site.register(Programme)
admin.site.register(Trimestre)
admin.site.register(Information_Personnelle)
admin.site.register(Paiement)
admin.site.register(Coordonne_Bancaire)

class DocumentFournirAdmin(admin.ModelAdmin):
    list_display = ('id', 'pdf_link_releve_note', 'pdf_link_attestation', 'pdf_link_lettre_motivation', 'pdf_link_piece_identite', 'pdf_link_acte_Naissance')

    def pdf_link_releve_note(self, obj):
        return obj.pdf_link('releve_note')

    pdf_link_releve_note.allow_tags = True
    pdf_link_releve_note.short_description = 'Releve Note'

    def pdf_link_attestation(self, obj):
        return obj.pdf_link('attestation')

    pdf_link_attestation.allow_tags = True
    pdf_link_attestation.short_description = 'Attestation'

    def pdf_link_lettre_motivation(self, obj):
        return obj.pdf_link('lettre_motivation')

    pdf_link_lettre_motivation.allow_tags = True
    pdf_link_lettre_motivation.short_description = 'Lettre Motivation'

    def pdf_link_piece_identite(self, obj):
        return obj.pdf_link('piece_identite')

    pdf_link_piece_identite.allow_tags = True
    pdf_link_piece_identite.short_description = 'Piece Identite'

    def pdf_link_acte_Naissance(self, obj):
        return obj.pdf_link('acte_Naissance')

    pdf_link_acte_Naissance.allow_tags = True
    pdf_link_acte_Naissance.short_description = 'Acte Naissance'

    def view_document(self, request, document_id, field_name):
        document = Document_Fournir.objects.get(pk=document_id)
        file_field = getattr(document, field_name)
        response = FileResponse(file_field.open(), content_type='application/pdf')
        return response

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:document_id>/<slug:field_name>/', self.admin_site.admin_view(self.view_document), name='view_document'),
        ]
        return custom_urls + urls
admin.site.register(Document_Fournir, DocumentFournirAdmin)
from .traitement import traiter_documents
class Traite_Admission(admin.ModelAdmin):
    actions = ['traiter_avec_IA']
    def traiter_avec_IA(self, request, queryset):
        for demande in queryset:
            traiter_documents(demande)
        self.message_user(request, "Les demandes sélectionnées ont été traitées avec l'IA.")
    traiter_avec_IA.short_description = "Traiter les demandes sélectionnées avec l'IA"
admin.site.register(Demander_Admission, Traite_Admission)
