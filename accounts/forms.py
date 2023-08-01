from django import forms
from .models import Account, UserProfile
from django import forms
from django.contrib.auth import authenticate
from .models import Account




class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = Account
        fields = [ 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ( 'phone_number',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ( 'city',  'profile_picture',)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'



class LoginForm(forms.Form):
    
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Email Address',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control',
    }))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Authenticate the user with the email and password
            user = authenticate(request=None, email=email, password=password)

            if user is None:
                raise forms.ValidationError(
                    "Invalid email or password. Please try again."
                )
        else:
            raise forms.ValidationError(
                "Both email and password are required."
            )