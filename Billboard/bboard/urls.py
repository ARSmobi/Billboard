from django.urls import path
from .views import (AdvertisementListView,
                    AdvertisementDetailView,
                    about_view,
                    contacts_view,
                    AdvertisementCreateView,
                    LkDetailView,
                    AdvertisementUpdateView,
                    AdvertisementDeleteView,
                    ReactionCreateView,
                    ReactionDetailView,
                    ReactionDeleteView,
                    ReactionListView)

urlpatterns = [
    path('advertisements/', AdvertisementListView.as_view(), name='index'),
    path('about/', about_view, name='about'),
    path('contacts/', contacts_view, name='contacts'),
    path('advertisement/<int:pk>', AdvertisementDetailView.as_view(), name='adv_detail'),
    path('advertisement/create/', AdvertisementCreateView.as_view(), name='adv_create'),
    path('advertisement/<int:pk>/edit', AdvertisementUpdateView.as_view(), name='adv_edit'),
    path('advertisement/<int:pk>/delete', AdvertisementDeleteView.as_view(), name='adv_delete'),
    path('lk/<int:pk>', LkDetailView.as_view(), name='lk'),
    path('advertisement/<int:pk>/reactions', ReactionListView.as_view(), name='reaction_list'),
    path('reaction/<int:pk>', ReactionDetailView.as_view(), name='reaction_detail'),
    path('advertisement/<int:advertisement_id>/reaction/', ReactionCreateView.as_view(), name='reaction_create'),
    path('reaction/delete/<int:pk>', ReactionDeleteView.as_view(), name='reaction_delete'),
]
