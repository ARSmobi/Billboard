from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.http import urlencode
from django.views.generic import CreateView, DeleteView
from pyexpat.errors import messages

from .forms import SignUpForm, LoginForm, VerificationForm
from .models import VerificationCode
from bboard.models import User
from Billboard.custom_settings import *


class UserSignUpView(CreateView):
    form_class = SignUpForm
    # success_url = reverse('verification')
    model = User
    template_name = 'accounts/signup.html'

    def get_success_url(self):
        return reverse('verification', args=[self.object.id])

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
            'Verification Code',
            f'Your verification code is {verification_code.code}',
            'from@example.com',
            [user.email],
        )

        # url = reverse('verification', args=[user.id])
        return super().form_valid(form)


def verification_view(request, user_id):
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
    return render(
        request,
        'accounts/verification.html',
        {'form': form, 'have_code': have_code, 'user_id': user_id, 'code_time_delta': int(code_time_delta)}
    )


def send_verification_code(request, user_id, action):
    user = User.objects.get(id=user_id)
    if action == 'signup':
        url = reverse('verification', args=[user_id])
        minutes = REGISTRATION_CODE_LIFETIME
    else:
        url = reverse('delete_account', args=[user_id])
        minutes = DELETE_ACCOUNT_CODE_LIFETIME
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
                url = reverse('verification', args=[user.id])
                return redirect(url)
        return super().form_invalid(form)


class UserLogoutView(LogoutView):
    template_name = 'accounts/logout-confirm.html'
    next_page = 'login'


class UserDeleteView(DeleteView):
    model = User
    form_class = VerificationForm
    template_name = 'accounts/delete-account.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_id'] = self.kwargs['pk']
        context['have_code'] = VerificationCode.objects.filter(user=self.object.id).exists()
        context['code_time_delta'] = 0
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
