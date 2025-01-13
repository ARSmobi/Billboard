from gettext import gettext as _

from allauth.core.internal.httpkit import redirect
from django import forms
from bboard.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import VerificationCode


class SignUpForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": _("Два пароля не совпадают"),
        "username_exists": _("Пользователь с таким именем уже существует"),
        "email_exists": _("Пользователь с таким email уже существует"),
    }
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput,
        help_text=_('Имя пользователя должно быть уникальным и не должно содержать пробелы.'))
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput,
        help_text=_('Введите ваш email'))
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput,
        help_text=_('Пожалуйста, введите пароль'))
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput,
        help_text=_('Пожалуйста, подтвердите пароль'))

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
            raise ValidationError(_('Такой пользователь уже существует'))
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("Пароли не совпадают"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _("Неверный логин или пароль"),
        "inactive": _("Пользователь заблокирован"),
    }
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError(_('Пользователь не найден'))
        if user and not user.is_active:
            url = reverse('verification', args=[user.id])
            return redirect(url)
        return cleaned_data


class VerificationForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not VerificationCode.objects.filter(code=code).exists():
            raise forms.ValidationError(_("Не верный проверочный код"))
        return code


class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_('Пользователь с таким email не существует'))
        return email


class PasswordResetForm(forms.Form):
    error_messages = {
        "password_mismatch": _("Два пароля не совпадают"),
    }
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput,
        help_text=_('Пожалуйста, введите пароль'))
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput,
        help_text=_('Пожалуйста, подтвердите пароль'))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("Пароли не совпадают"))
        return password2

    def save(self):
        self.instance.set_password(self.cleaned_data['password1'])
        self.instance.save()
        VerificationCode.objects.get(user_id=self.instance.id).delete()  # удаляем проверочный код
        return self.instance
