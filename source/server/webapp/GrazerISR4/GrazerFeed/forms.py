from django import forms
import datetime

class OptionsPage(forms.Form):
    fromdate = forms.DateField()
    todate = forms.DateField()
    fromtime = forms.TimeField()
    totime = forms.TimeField()
    res = forms.IntegerField()
    fps = forms.IntegerField()

    def check_date(self):
        from_date = self.cleaned_data['fromdate']
        to_date = self.cleaned_data['todate']

        if from_date > datetime.date.today() or to_date > datetime.date.today() or to_date < from_date:
            list_date = None
        else:
            list_date = [from_date, to_date]
        return list_date