from django import forms
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class OptionsForm(forms.Form):
    FromDate = forms.DateField()
    ToDate = forms.DateField()
    FromTime = forms.TimeField()
    ToTime = forms.TimeField()
    Resolution = forms.IntegerField()
    FPS = forms.IntegerField()

    def check_date(self):
        fromdate = self.cleaned_data['FromDate']
        todate = self.cleaned_data['ToDate']

        if fromdate > datetime.date.today() or todate > datetime.date.today() or todate < fromdate:
            list_date = None
        else:
            list_date = [fromdate, todate]
        return list_date

    def check_time(self):
        fromtime = self.cleaned_data['FromTime']
        totime = self.cleaned_data['ToTime']
        list_time = [fromtime, totime]


    def check_res_fps(self):
        res = self.cleaned_data['Resolution']
        fps = self.cleaned_data['FPS']
        list_res_fps = [res, fps]
        return list_res_fps

