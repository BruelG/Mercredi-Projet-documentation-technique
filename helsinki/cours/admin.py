from django.contrib import admin
from .models import Cours , Prerequis , Cours_Etudiants, Cours_Session
# Register your models here.


class PrerequisInline(admin.StackedInline):
    model = Prerequis
    fk_name = 'from_cours'

class CoursAdmin(admin.ModelAdmin):
    filter_horizontal = ('prerequis',)
    inlines = [PrerequisInline]



admin.site.register(Cours, CoursAdmin)
admin.site.register(Cours_Etudiants)
admin.site.register(Cours_Session)
