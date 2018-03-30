from django import forms
import datetime

class OptionsPage(forms.Form):
    fromdate = forms.DateField()
    todate = forms.DateField()
    fromtime = forms.TimeField()
    totime = forms.TimeField()
    res = forms.IntegerField()
    fps = forms.IntegerField()

class LoginPage(forms.Form):
    User = forms.CharField()
    Password = forms.CharField()