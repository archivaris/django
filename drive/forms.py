from django import forms
from django.contrib.auth.models import User

from .models import Student, Grade, Course, Permit, payment_deadlines


# Add/Edit User profile
class UpdateProfile(forms.ModelForm):
    is_super = forms.BooleanField(required=False)

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'email', 'course', 'permit', 'country', 'city', 'user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'hidden': True})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['permit'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['course'].widget.attrs.update({'class': 'full-width', 'hidden': True, 'required': False})


# Sign up form
class SignUpForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean_username(self):
        try:
            User.objects.get(username__iexact=self.username)
            raise forms.ValidationError('User already exists')
        except User.DoesNotExist:
            return self.username

    def clean_password(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')

        if pw1 and pw2 and pw1 == pw2:
            return pw1
        raise forms.ValidationError("Password doesn't match")


# Select teachers for a specific course
class SelectInstructorsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.ModelMultipleChoiceField(queryset=Student.objects.all())
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})


class GradeStudentsForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('student', 'grade',)

    def __init__(self, *args, **kwargs):
        super(GradeStudentsForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs.update({'class': 'form-control'})
        self.fields['grade'].widget.attrs.update({'class': 'form-control'})


class DateInput(forms.DateInput):
    input_type = 'date'


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['permit'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['cost'].widget.attrs.update({'class': 'form-control'})


class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})


class DeadlinesForm(forms.ModelForm):
    class Meta:
        model = payment_deadlines
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

#
