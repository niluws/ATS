from django.contrib import admin
from .models import NewPositionModel


@admin.register(NewPositionModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('position_title', 'contract_type', 'reason', 'education_level', 'experience_level', 'department',
                    'quantity', 'budget')
    list_filter = ('status', 'hr_approval', 'td_approval')
