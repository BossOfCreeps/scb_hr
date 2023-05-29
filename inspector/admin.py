from django.contrib import admin

from inspector.models import Resume, ResumeCheck, ResumeFile, Interview

admin.site.register(Interview)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    class ResumeFileAdmin(admin.StackedInline):
        model = ResumeFile

    class ResumeCheckAdmin(admin.StackedInline):
        model = ResumeCheck
        readonly_fields = ['created']

    inlines = [ResumeFileAdmin, ResumeCheckAdmin]
    readonly_fields = ['created']
