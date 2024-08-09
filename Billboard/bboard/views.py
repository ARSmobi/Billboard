from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AdvertisementForm, ReactionForm
from .models import Advertisement, Reaction


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'bboard/index.html'
    context_object_name = 'advertisements'


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'bboard/adv-detail.html'
    context_object_name = 'adv'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reactions'] = Reaction.objects.filter(advertisement=self.object).count()
        return context


def about_view(request):
    return render(request, 'bboard/about.html', {})


def contacts_view(request):
    return render(request, 'bboard/contacts.html', {})


class AdvertisementCreateView(CreateView):
    model = Advertisement
    template_name = 'bboard/adv-edit.html'
    form_class = AdvertisementForm

    def form_valid(self, form):
        adv = form.save(commit=False)
        adv.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lk', kwargs={'pk': self.request.user.id})


class AdvertisementUpdateView(UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'bboard/adv-edit.html'
    context_object_name = 'advertisement'

    def get_success_url(self):
        return reverse('lk', kwargs={'pk': self.request.user.id})


class LkDetailView(ListView):
    model = Advertisement
    template_name = 'bboard/lk.html'
    context_object_name = 'advertisements'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisements'] = Advertisement.objects.filter(user=self.request.user)
        return context


class AdvertisementDeleteView(DeleteView):
    model = Advertisement
    template_name = 'adv-delete.html'
    success_url = '/advertisements/'


class ReactionCreateView(CreateView):
    model = Reaction
    template_name = 'bboard/reaction.html'
    form_class = ReactionForm
    success_url = '/advertisements/'

    def form_valid(self, form):
        adv = get_object_or_404(Advertisement, id=self.kwargs['advertisement_id'])
        form.instance.advertisement = adv
        form.instance.user = self.request.user
        return super().form_valid(form)


class ReactionListView(DetailView):
    model = Advertisement
    template_name = 'bboard/reaction-list.html'
    context_object_name = 'advertisement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reactions'] = Reaction.objects.filter(advertisement=self.object)
        return context


class ReactionDetailView(DetailView):
    pass


class ReactionDeleteView(DeleteView):
    pass
