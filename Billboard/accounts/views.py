from django.utils.translation import gettext as _

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import SignUpForm, LoginForm, VerificationForm, PasswordResetEmailForm, PasswordResetForm
from .models import VerificationCode
from bboard.models import User
from Billboard.custom_settings import *


class UserSignUpView(CreateView):
    form_class = SignUpForm
    # success_url = reverse('verification')
    model = User
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        return reverse('verification', args=[self.object.id, 'signup'])

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        # создание проверочного кода и времени для его удаления
        verification_code = (
            VerificationCode.objects.create(
                user=user,
                delete_at=timezone.now() + timezone.timedelta(minutes=REGISTRATION_CODE_LIFETIME))
        )

        send_mail (
            _('Код подтверждения регистрации'),
            _(f'Ваш код подтверждения: {verification_code.code}. Скопируйте его и используйте для продолжения регистрации.'),
            'from@example.com',
            [user.email],
        )

        # url = reverse('verification', args=[user.id])
        return super().form_valid(form)


def verification_view(request, user_id, action):
    user = User.objects.get(id=user_id)
    have_code = VerificationCode.objects.filter(user=user).exists()
    code_time_delta = 0  # Время жизни кода в минутах
    if have_code:
        code_delete_at = VerificationCode.objects.get(user=user).delete_at
        code_time_delta = (code_delete_at - timezone.now()).seconds / 60  # Время жизни кода в минутах
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            verification_code = VerificationCode.objects.get(code=code)
            user = verification_code.user
            user.is_active = True
            user.save()
            verification_code.delete()
            return redirect('login')
    else:
        form = VerificationForm()
    return render(request,
        'accounts/verification.html',
        {
            'form': form,
            'have_code': have_code,
            'user_id': user_id,
            'code_time_delta': int(code_time_delta),
            'action': action
        })



def send_verification_code(request, user_id, action):
    user = User.objects.get(id=user_id)
    if action == 'signup':
        url = reverse('verification', args=[user_id, action])
        minutes = REGISTRATION_CODE_LIFETIME
    elif action == 'delete':
        url = reverse('delete_account', args=[user_id, action])
        minutes = DELETE_ACCOUNT_CODE_LIFETIME
    elif action == 'password_reset':
        url = reverse('password_reset_verification', args=[user_id, action])
        minutes = PASSWORD_RESET_CODE_LIFETIME
    else:
        return HttpResponse('Invalid action')
    verification_code = (
        VerificationCode.objects.create(
            user=user,
            delete_at=timezone.now() + timezone.timedelta(minutes=minutes))
    )
    send_mail(
        'Verification Code',
        f'Your verification code is {verification_code.code}',
        'from@example.com',
        [user.email],
    )
    return redirect(url)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user and not user.is_active:
                url = reverse('verification', args=[user.id, 'signup'])
                return redirect(url)
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout-confirm.html'
    next_page = 'login'


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    form_class = VerificationForm
    template_name = 'accounts/verification.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.kwargs['pk']
        context['have_code'] = VerificationCode.objects.filter(user=self.object.id).exists()
        context['code_time_delta'] = 0
        context['action'] = 'delete'
        if VerificationCode.objects.filter(user=self.object.id).exists():
            code_delete_at = VerificationCode.objects.get(user=self.object.id).delete_at
            context['code_time_delta'] = int((code_delete_at - timezone.now()).seconds / 60)
        return context

    def form_valid(self, form):
        code = form.cleaned_data['code']
        verification_code = VerificationCode.objects.get(code=code)
        user = verification_code.user
        user.delete()
        verification_code.delete()
        return super().form_valid(form)


def password_reset_email(request):
    if request.method == 'POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                url = reverse('password_reset_verification', args=[user.id, 'password_reset'])
                return redirect(url)
            else:
                raise ValidationError(_('Пользователь с таким email не найден'))
    else:
        form = PasswordResetEmailForm()
    return render(request, 'accounts/password-reset-email.html', {'form': form})


def password_reset_verification(request, user_id, action):
    user = User.objects.get(id=user_id)
    have_code = VerificationCode.objects.filter(user=user).exists()
    code_time_delta = 0
    if have_code:
        code_delete_at = VerificationCode.objects.get(user=user).delete_at
        code_time_delta = (code_delete_at - timezone.now()).seconds / 60
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            verification_code = VerificationCode.objects.get(code=code)
            user = verification_code.user
            url = reverse('password_reset', args=[user.id])
            return redirect(url)
    else:
        form = VerificationForm()
    return render(request,
                  'accounts/verification.html',
                  {'form': form,
                   'user_id': user_id,
                   'have_code': have_code,
                   'code_time_delta': int(code_time_delta),
                   'action': action})


class PasswordResetView(UpdateView):
    model = User
    form_class = PasswordResetForm
    template_name = 'accounts/password-reset.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if not VerificationCode.objects.filter(user=user).exists():
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs['user_id'])
