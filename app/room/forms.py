from django import forms
from django.utils.translation import gettext as _
from room.models import Scheduling
from datetime import datetime
from room.helpers import date_validation


class SchedulingForm(forms.ModelForm):
    class Meta:
        model = Scheduling
        fields = '__all__'

    def clean(self):
        object_id = (self.instance.id if self.instance else None)
        room = self.cleaned_data.get('room')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        validation = date_validation(room, object_id, start_date, end_date)
        if validation:
            raise forms.ValidationError(','.join(validation))
        return self.cleaned_data
