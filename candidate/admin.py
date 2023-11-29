from django.contrib import admin

from .models import CandidateModel, PreferencesModel, EducationModel, ExperiencesModel, AppointmentModel

admin.site.register(PreferencesModel)
admin.site.register(EducationModel)
admin.site.register(ExperiencesModel)
admin.site.register(AppointmentModel)

class AppointmentModelInline(admin.TabularInline):
    model = AppointmentModel
    extra = 0


@admin.register(CandidateModel)
class CandidateModelAdmin(admin.ModelAdmin):
    inlines = (AppointmentModelInline,)
    list_display = ('name', 'score',)
    list_editable = ('score',)
