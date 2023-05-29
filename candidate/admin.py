from django.contrib import admin

from account.models import CustomUser
from candidate.models import Education, Contact, WorkExperience


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    class ContactAdmin(admin.StackedInline):
        model = Contact

    class WorkExperienceAdmin(admin.StackedInline):
        model = WorkExperience

    class EducationAdmin(admin.StackedInline):
        model = Education

    inlines = [ContactAdmin, WorkExperienceAdmin, EducationAdmin]
