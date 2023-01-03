from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class NewsFilter(FilterSet):
    added_after = DateFilter(
        field_name='post_date',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = Post
        fields = {
           'post_title': ['icontains'],
           'post_category': ['exact'],
            }
