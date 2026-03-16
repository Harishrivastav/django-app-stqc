from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class EngineerRegisterForm(UserCreationForm):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class':'form-control'}
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class':'form-control'}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control'}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class':'form-control'}
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

from .models import TestingJob

class ProgressForm(forms.ModelForm):

    class Meta:
        model = TestingJob
        fields = ['progress','status','report_file']


from .models import TestingJob


class JobAssignForm(forms.ModelForm):

    class Meta:

        model = TestingJob

        fields = [
            'SRF',
            'job_no',
            'received_date',
            'job_details',
            'assigned_to',
            'amount'
        ]

        widgets = {

            'received_date': forms.DateInput(
                attrs={'type':'date'}
            ),

            'job_details': forms.Textarea(
                attrs={'rows':3}
            )

        }