from django import forms
import datetime
from django.http import HttpResponse
from django.core import validators

class OptionsPage(forms.Form):
    fromdate = forms.DateField()
    todate = forms.DateField()
    fromtime = forms.TimeField()
    totime = forms.TimeField()
    res = forms.IntegerField()
    fps = forms.DecimalField()
    interval = forms.TimeField()

    def clean(self):
        from_date = self.cleaned_data['fromdate']
        to_date = self.cleaned_data['todate']
        if from_date > datetime.date.today() or to_date > datetime.date.today() or to_date < from_date:
            raise forms.ValidationError("Invalid date pair")
        
    
class LoginPage(forms.Form):
    Username = forms.CharField()
    Password = forms.CharField()
