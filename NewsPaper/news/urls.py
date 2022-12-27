from django.urls import path
from .views import NewsList, ViewNews


urlpatterns = [
   path('news/', NewsList.as_view()),
   path('news/<int:pk>', ViewNews.as_view()),
]