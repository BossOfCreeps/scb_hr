from django import forms

from inspector.models import Interview


class VacancyApproveForm(forms.Form):
    resume = forms.IntegerField()
    approve_text = forms.CharField(required=False)


class VacancyDenyForm(forms.Form):
    resume = forms.IntegerField()
    deny_text = forms.CharField(required=False)


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        exclude = ["resume"]
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'finish_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
