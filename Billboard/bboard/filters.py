from django_filters import FilterSet, filters
from .models import Advertisement


class AdvertisementFilter(FilterSet):
    dateCreation = filters.DateFilter(label='Дата', lookup_expr='gt')
    title = filters.CharFilter(label='Название', lookup_expr='iregex')
    user = filters.CharFilter(label='Автор', lookup_expr='exact')

    class Meta:
        model = Advertisement
        fields = ['user', 'title', 'dateCreation']
