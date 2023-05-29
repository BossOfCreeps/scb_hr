from django import forms

select_widget = forms.Select(attrs={'data-live-search': 'true'})
select_multiple_widget = forms.SelectMultiple(attrs={'data-live-search': 'true'})
