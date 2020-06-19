from django import forms
from .models import Users

class UserLoginForm(forms.Form):
   
    class Meta:
        CHOICES=(('is_mentor','is_mentor'),
                'is_student','is_student')
        model = Users
        fields = ['Username','Password']
        status = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxInput())
