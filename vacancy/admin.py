from django.contrib import admin

from vacancy.models import VacancyCheck, Vacancy, Office, City, EmploymentType, WorkYears, Specialisation

admin.site.register(Office)
admin.site.register(City)

admin.site.register(WorkYears)
admin.site.register(EmploymentType)
admin.site.register(Specialisation)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    class VacancyCheckAdmin(admin.StackedInline):
        model = VacancyCheck

    inlines = [VacancyCheckAdmin]
    fields = ['created']
