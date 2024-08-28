from django.urls import path
from django.views.generic import TemplateView

from .views import (AdvertisementListView, AdvertisementDetailView, HomeView,
                    AdvertisementCreateView, AdvertisementUpdateView, AdvertisementDeleteView,
                    LkDetailView, LkSettingsDetailView, LkSettingsUpdateView, SettingsAvatarView, change_avatar_view,
                    about_view, contacts_view,
                    ReactionCreateView, ReactionDetailView, ReactionDeleteView,
                    ReactionListView, MyReactionslistView, MyReactionDetailView,
                    reaction_accept,
                    ReactionUpdateView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('advertisements/', AdvertisementListView.as_view(), name='index'),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('advertisement/<int:pk>', AdvertisementDetailView.as_view(), name='adv_detail'),
    path('advertisement/create/', AdvertisementCreateView.as_view(), name='adv_create'),
    path('advertisement/<int:pk>/edit', AdvertisementUpdateView.as_view(), name='adv_edit'),
    path('advertisement/<int:pk>/delete', AdvertisementDeleteView.as_view(), name='adv_delete'),
    path('lk/<int:pk>', LkDetailView.as_view(), name='lk'),
    path('lk/<int:pk>/settings', LkSettingsDetailView.as_view(), name='lk_settings'),
    path('lk/<int:pk>/avatar', SettingsAvatarView.as_view(), name='settings_avatar'),
    path('lk/<int:pk>/change_avatar', change_avatar_view, name='change_avatar'),
    path('lk/<int:pk>/settings/edit', LkSettingsUpdateView.as_view(), name='lk_settings_edit'),
    path('lk/<int:pk>/my_reactions', MyReactionslistView.as_view(), name='my_reactions'),
    path('lk/adv/<int:pk>/my_reaction', MyReactionDetailView.as_view(), name='my_reaction'),
    path('advertisement/<int:pk>/reactions', ReactionListView.as_view(), name='reaction_list'),
    path('reaction/<int:pk>', ReactionDetailView.as_view(), name='reaction_detail'),
    path('advertisement/<int:advertisement_id>/reaction/', ReactionCreateView.as_view(), name='reaction_create'),
    path('reaction/<int:pk>/delete', ReactionDeleteView.as_view(), name='reaction_delete'),
    path('reaction/<int:pk>/edit', ReactionUpdateView.as_view(), name='reaction_edit'),
    path('reaction/<int:reaction_id>/accept', reaction_accept, name='reaction_accept'),
    path('access_denied/', TemplateView.as_view(template_name='bboard/403.html'), name='page403'),
]
