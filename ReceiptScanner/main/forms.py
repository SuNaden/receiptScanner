from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class RegisterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for fieldname, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if (fieldname == "email"): field.widget.attrs['placeholder'] = 'E-Mail'
            if (fieldname == "username"): field.widget.attrs['placeholder'] = 'Username'
            if (fieldname == "password1"): field.widget.attrs['placeholder'] = 'Password'
            if (fieldname == "password2"): field.widget.attrs['placeholder'] = 'Confirm Password'

    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
   

    def clean(self):
        if (self.cleaned_data.get('password1') != self.cleaned_data.get('password2')):
            raise ValidationError("Passwords do not match.")

        return self.cleaned_data