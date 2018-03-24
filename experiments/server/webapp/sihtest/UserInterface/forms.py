from django import forms
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class NameForm(forms.Form):
    FromDate = forms.DateField()
    ToDate = forms.DateField()
    FromTime = form.TimeField()

    def check_date(self):
        fd = self.cleaned_data['FromDate']
        td = self.cleaned_data['ToDate']
        ft = self.cleaned_data['FromTime']
        if fd > datetime.date.today() or td > datetime.date.today() or td < fd:
            print('In forms if')
            list = None
        else:
            list = [fd, td]
        return list