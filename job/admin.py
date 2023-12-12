from django.contrib import admin

from .models import Job, JobRequirement, Role, NewRequestModel, Requirement


@admin.register(NewRequestModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                    'quantity', 'budget', 'hr_approval', 'assigned_to_td')
    list_filter = ('status', 'hr_approval', 'td_approval', 'assigned_to_td')


admin.site.register(Role)

admin.site.register(Requirement)


class JobRequirementInline(admin.TabularInline):
    model = JobRequirement
    extra = 0


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = (JobRequirementInline,)
