from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class NameForm(forms.Form):
    FromDate = datetime.datetime(year, month, day)
    FromDate = FromDate.strftime("%d/%m/%Y")

    def check_date(self):
        date = self.cleaned_data['FromDate']
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        return date