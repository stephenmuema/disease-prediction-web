from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import User, Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': 'example@domain.com', 'style': 'text-align:center'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'eg(Michp@57r13$)', 'style': 'text-align:center'}),
        label='Password')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'eg(Michp@57r13$)', 'style': 'text-align:center'}),
        label='Password')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Jane', 'style': 'text-align:center'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Doe', 'style': 'text-align:center'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=254)

    class Meta:
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }


class NewPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD'}), max_length=20,
                                label='PASSWORD')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'PASSWORD CONFIRMATION'}),
                                max_length=20, label='PASSWORD CONFIRMATION')

    class Meta:
        fields = ('password1', 'password2')


class ContactUsForm(forms.Form):
    sender_name = forms.CharField(required=True,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    sender_mail = forms.EmailField(required=True,
                                   widget=forms.EmailInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    mail_subject = forms.CharField(required=True,
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Your Subject'}))

    mail_message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Message here....', "rows": 7, "cols": 30}))


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'style': 'text-align:center',
               'placeholder': 'example@domain.com', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'style': 'text-align:center',
            'placeholder': 'PASSWORD',
        }
    ))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address']
        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),

        }


class ProfileAccountForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, disabled=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
