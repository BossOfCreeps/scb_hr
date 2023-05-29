from django import forms


class SuperjobForm(forms.Form):
    text = forms.CharField(label="Запрос", required=False)
    town = forms.CharField(label="Город", required=False)
    count = forms.IntegerField(label="Число вакансий", required=False)
    page = forms.IntegerField(label="Страница вакансий", required=False)
