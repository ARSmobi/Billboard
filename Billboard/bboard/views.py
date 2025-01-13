from os import walk
from django.utils.translation import activate, get_language, get_language_info, gettext as _

import django_filters
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import viewsets, permissions

from .forms import AdvertisementForm, ReactionForm, UserSettingsForm
from .models import Advertisement, Reaction, User, Subscription, Category
from .filters import AdvertisementFilter
from .mixins import AuthorRequiredMixin
from .serializers import UserSerializer, AdvertisementSerializer, CategorySerializer, ReactionSerializer
from .translations import TRANSLATIONS


class HomeView(TemplateView):
    """Домашняя страница"""
    template_name = 'bboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lang = get_language()
        context['text'] = TRANSLATIONS.get(lang, {}).get('home_text', '')
        return context


class AdvertisementListView(ListView):
    """Список объявлений"""
    model = Advertisement
    filterset_class = AdvertisementFilter
    template_name = 'bboard/index.html'
    context_object_name = 'advertisements'
    paginate_by = 5
    ordering = '-dateCreation'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', 'dateCreation')
        if sort_by == 'date_ask':
            queryset = queryset.order_by('dateCreation')
        else:
            queryset = queryset.order_by('-dateCreation')
        self.filterset = AdvertisementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['filter'] = AdvertisementFilter(self.request.GET, queryset=self.get_queryset())
        return context


class UserAdvertisementListView(ListView):
    """Список объявлений пользователя"""
    model = Advertisement
    filterset_class = AdvertisementFilter
    template_name = 'bboard/user-advs.html'
    context_object_name = 'advertisements'
    paginate_by = 5
    ordering = '-dateCreation'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.kwargs['user_id'])
        sort_by = self.request.GET.get('sort', 'dateCreation')
        if sort_by == 'date_ask':
            queryset = queryset.order_by('dateCreation')
        else:
            queryset = queryset.order_by('-dateCreation')
        self.filterset = AdvertisementFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['filter'] = AdvertisementFilter(self.request.GET, queryset=self.get_queryset())
        return context


class AdvertisementDetailView(DetailView):
    """Детальная страница объявления"""
    model = Advertisement
    template_name = 'bboard/adv-detail.html'
    context_object_name = 'adv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_subscribed'] = Subscription.objects.filter(tag=f'user{self.request.user.id}-user{self.object.user.id}').exists()
        context['reactions'] = Reaction.objects.filter(advertisement=self.object).count()
        context['have_reaction'] = Reaction.objects.filter(user=self.request.user.id, advertisement=self.object).exists()
        if Reaction.objects.filter(user=self.request.user, advertisement=self.kwargs['pk']).exists():
            context['reaction_id'] = Reaction.objects.get(user=self.request.user, advertisement=self.kwargs['pk']).id
        return context


def about_view(request):
    return render(request, 'bboard/about.html', {})


def contacts_view(request):
    return render(request, 'bboard/contacts.html', {})


class AdvertisementCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Страница создания объявления"""
    permission_required = ('bboard.add_advertisement',)
    model = Advertisement
    template_name = 'bboard/adv-edit.html'
    form_class = AdvertisementForm

    def form_valid(self, form):
        adv = form.save(commit=False)
        adv.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lk', kwargs={'pk': self.request.user.id})


class AdvertisementUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Страница редактирования объявления"""
    permission_required = ('bboard.change_advertisement',)
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'bboard/adv-edit.html'
    context_object_name = 'advertisement'

    def get_success_url(self):
        return reverse('lk', kwargs={'pk': self.request.user.id})


class AdvertisementDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Страница удаления объявления"""
    permission_required = ('bboard,delete_advertisement',)
    model = Advertisement
    template_name = 'bboard/adv-delete.html'
    success_url = '/advertisements/'


class LkDetailView(LoginRequiredMixin, ListView):
    """Страница личного кабинета со списком объявлений"""
    model = Advertisement
    template_name = 'lk/lk-advertisements.html'
    context_object_name = 'advertisements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisements'] = Advertisement.objects.filter(user=self.request.user)
        return context


class LkSettingsDetailView(DetailView):
    """Страница личного кабинета с настройками пользователя"""
    model = User
    template_name = 'lk/settings.html'
    context_object_name = 'user'


class LkSettingsUpdateView(UpdateView):
    """Страница редактирования настроек пользователя"""
    model = User
    template_name = 'lk/settings-edit.html'
    form_class = UserSettingsForm
    context_object_name = 'user'

    # def post(self, request, *args, **kwargs):
    #     form = UserSettingsForm(request.POST, instance=self.get_object())
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse('lk_settings'))
    #     return self.render_to_response({'form': form})

    def get_success_url(self):
        return reverse('lk_settings', kwargs={'pk': self.object.id})


class SettingsAvatarView(TemplateView):
    """Страница редактирования аватара"""
    template_name = 'lk/settings-avatar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avatar_dir_path = 'static/avatar'
        avatars = []
        for (dirpath, dirnames, filenames) in walk(avatar_dir_path):
            avatars.extend(filenames)
            break
        context['avatars'] = avatars
        return context


def change_avatar_view(request, pk):
    user = User.objects.get(id=pk)
    avatar = request.GET.get('avatar')
    user.avatar = avatar
    user.save()
    return redirect('lk_settings', request.user.id)


class ReactionCreateView(LoginRequiredMixin, CreateView):
    """Страница создания отклика"""
    model = Reaction
    template_name = 'bboard/reaction.html'
    form_class = ReactionForm
    success_url = '/advertisements/'

    def form_valid(self, form):
        adv = get_object_or_404(Advertisement, id=self.kwargs['advertisement_id'])
        form.instance.advertisement = adv
        form.instance.user = self.request.user

        subject = _('Отклик на объявление')
        message = _(f'На ваше объявление {adv.title} пользователь {self.request.user.username} оставил отклик.')
        from_email = 'note@site.ru'
        to_email = self.request.user.email
        send_mail(subject, message, from_email, [to_email])

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_adv'] = get_object_or_404(Advertisement, id=self.kwargs['advertisement_id'])
        context['have_reaction'] = Reaction.objects.filter(advertisement=self.kwargs['advertisement_id']).exists()
        return context


class ReactionUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    """Страница редактирования отклика"""
    model = Reaction
    form_class = ReactionForm
    template_name = 'bboard/reaction.html'
    context_object_name = 'reaction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_adv = get_object_or_404(Advertisement, id=self.object.advertisement.pk)
        context['current_adv'] = current_adv
        return context

    def get_success_url(self):
        current_adv = get_object_or_404(Advertisement, id=self.kwargs['pk'])
        return reverse('adv_detail', kwargs={'pk': current_adv.id})


class ReactionListView(LoginRequiredMixin, AuthorRequiredMixin, DetailView):
    """Страница со списком откликов"""
    model = Advertisement
    template_name = 'bboard/reaction-list.html'
    context_object_name = 'advertisement'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_date = self.request.GET.get('sort', 'dateCreation')
        if sort_date == 'date_ask':
            queryset = queryset.order_by('dateCreation')
        else:
            queryset = queryset.order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reactions'] = Reaction.objects.filter(advertisement=self.object)
        return context


class ReactionDetailView(LoginRequiredMixin, DetailView):
    """Страница отклика"""
    model = Reaction
    template_name = 'bboard/reaction-detail.html'
    context_object_name = 'reaction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reaction = Reaction.objects.get(id=self.kwargs['pk'])
        context['adv_author'] = get_object_or_404(Advertisement, id=reaction.advertisement.id).user.id
        return context


class ReactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Страница удаления отклика"""
    permission_required = ('bboard.delete_reaction',)
    model = Reaction
    template_name = 'bboard/reaction-delete.html'
    context_object_name = 'reaction'
    success_url = '/advertisements/'


def reaction_accept(request, reaction_id):
    """Функция принятия отклика"""
    reaction = Reaction.objects.get(pk=reaction_id)
    reaction.accept()
    url = reverse('reaction_detail', args=[reaction_id])
    return HttpResponseRedirect(url)


class MyReactionslistView(ListView):
    """Страница со списком откликов пользователя"""
    model = Advertisement
    template_name = 'lk/my-reactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reactions = Reaction.objects.filter(user=self.request.user.id)
        context['reactions'] = reactions
        advertisements = {}
        for reaction in reactions:
            r_id = reaction.advertisement.id
            advertisements[(Advertisement.objects.get(id=reaction.advertisement.id))] = r_id
        context['advertisements'] = advertisements

        return context


class MyReactionDetailView(LoginRequiredMixin, DetailView):
    """Страница отклика пользователя"""
    model = Advertisement
    template_name = 'bboard/my-reaction.html'
    context_object_name = 'adv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['my_reaction'] = Reaction.objects.get(user=self.request.user.id, advertisement=self.object)
        return context


def subscription(request, adv_id):
    """Функция подписки пользователя на категорию/пользователя"""
    user = User.objects.get(id=request.user.id)
    to = request.GET.get('to')
    content_type = None
    if to == 'user':
        content_type = ContentType.objects.get_for_model(User)
    elif request.GET.get('to') == 'category':
        content_type = ContentType.objects.get_for_model(Category)
    to_id = request.GET.get('to_id')
    action = request.GET.get('action')
    if action == 'create':
        Subscription.objects.create(user=user, content_type=content_type, object_id=to_id, tag=f'user{user.pk}-{to}{to_id}')
    else:
        Subscription.objects.filter(tag=f'user{user.pk}-{to}{to_id}').delete()
    url = reverse('adv_detail', args=[adv_id])
    return HttpResponseRedirect(url)


# ViewSets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category_id', 'user_id']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ReactionViewSet(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['user_id', 'advertisement_id']
