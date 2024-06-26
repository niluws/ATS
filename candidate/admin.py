from django.contrib import admin

from .models import CandidateModel, PreferencesModel, EducationModel, ExperiencesModel, AppointmentModel, StatusModel

admin.site.register(PreferencesModel)
admin.site.register(EducationModel)
admin.site.register(ExperiencesModel)
admin.site.register(AppointmentModel)
admin.site.register(StatusModel)


class StatusModelInline(admin.TabularInline):
    model = StatusModel
    extra = 0


class AppointmentModelInline(admin.TabularInline):
    model = AppointmentModel
    extra = 0


@admin.register(CandidateModel)
class CandidateModelAdmin(admin.ModelAdmin):
    inlines = (AppointmentModelInline, StatusModelInline)
    list_display = ('name', 'score','PDF_score','job')
    list_editable = ('score','PDF_score')
