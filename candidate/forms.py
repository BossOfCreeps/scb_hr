from django import forms

from candidate.models import WorkExperience, Education, Contact
from inspector.models import Resume, ResumeFile


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        exclude = ["candidate"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'finish_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ["candidate"]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'finish_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ["candidate"]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        _clean = super().clean
        return [_clean(d, initial) for d in data] if isinstance(data, (list, tuple)) else _clean(data, initial)


class CandidateVacancyRequestForm(forms.ModelForm):
    files = MultipleFileField(label="Приложения", required=False)

    class Meta:
        model = Resume
        fields = ["cv", "files"]


class ResumeFileForm(forms.ModelForm):
    class Meta:
        model = ResumeFile
        exclude = ["resume"]
