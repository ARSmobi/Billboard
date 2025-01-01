from django import forms
from bboard.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": "Два пароля не совпадают",
        "username_exists": "Пользователь с таким именем уже существует",
        "email_exists": "Пользователь с таким email уже существует",
    }
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput,
        help_text='Имя пользователя должно быть уникальным и не должно содержать пробелы.')
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput,
        help_text='Введите ваш email')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text='Пожалуйста, введите пароль')
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput,
        help_text='Пожалуйста, подтвердите пароль')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Такой пользователь уже существует')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class VerificationForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))