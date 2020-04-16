from crispy_forms.bootstrap import Tab, TabHolder
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (Layout, Field,
                                 ButtonHolder, Submit)
from django.forms import ModelForm

from .models import Student


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'roll',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            TabHolder(
                Tab('Personal Info',
                    'name',
                    'email',
                    ),
                Tab('Board Info',
                    Field('roll', ),
                    )
            ),
            ButtonHolder(
                Submit('submit', 'Admit Student',
                       )
            )
        )
