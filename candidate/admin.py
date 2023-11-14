from django.contrib import admin
from .models import CandidateModel,PreferencesModel,EducationModel

admin.site.register(CandidateModel)
admin.site.register(PreferencesModel)
admin.site.register(EducationModel)
