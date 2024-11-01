from datetime import datetime
from django.forms.widgets import SelectDateWidget, TextInput
from django.db.models import Min
from django_filters import FilterSet, filters
from .models import Advertisement


class AdvertisementFilter(FilterSet):
    year = datetime.now().year
    min_date = Advertisement.objects.aggregate(Min('dateCreation'))['dateCreation__min']
    dateCreation = filters.DateFilter(label='Дата', lookup_expr='gt', widget=SelectDateWidget(attrs={'class': 'col-xxl-5'}, years=(min_date.year - 1, year)))
    title = filters.CharFilter(label='Название', lookup_expr='iregex', widget=TextInput(attrs={'class': 'col-xxl-4'}))
    user = filters.CharFilter(label='Автор', lookup_expr='exact', widget=TextInput(attrs={'class': 'col-xxl-3'}))

    class Meta:
        model = Advertisement
        fields = ['user', 'title', 'dateCreation']
