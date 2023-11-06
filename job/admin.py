from django.contrib import admin
from .models import Job, JobSkill,Role,NewPositionModel


@admin.register(NewPositionModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                    'quantity', 'budget','hr_approval','assigned_to_td')
    list_filter = ('status', 'hr_approval', 'td_approval','assigned_to_td')

admin.site.register(Role)

class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = (JobSkillInline,)
