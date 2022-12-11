from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.widgets import PhoneNumberPrefixWidget

# import the model here to populate the form
from django.contrib.auth import get_user_model
User = get_user_model()


def validate_email(email):
    if not User.objects.filter(email = email).first():
        raise forms.ValidationError('Incorrect email or password')


class RegisterForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class':'form-control', 'placeholder':'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class':'form-control', 'placeholder':'Repeat Password'
        })

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', }),
            'phone': PhoneNumberPrefixWidget(
                    country_choices=[
                        ("CA", "Canada"),
                        ("NG", "Nigeria"),
                    ], 
                    attrs={'class':'form-control d-inline', 'placeholder':'Phone',})
        }


class LoginForm(forms.Form):
    error_class = 'is-invalid'
    email = forms.EmailField(label='Email',
                            max_length=70,
                            validators= [validate_email],
                            widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                            }))
    password = forms.CharField(label="Password",
                            min_length=6,
                            widget=forms.PasswordInput(attrs={
                                'class': 'form-control'
                            }))