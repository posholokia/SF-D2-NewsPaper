from django.urls import path
from .views import NewsList, ViewNews, SearchNews, PostCreate, PostUpdate, PostDelete

urlpatterns = [
   path('news/', NewsList.as_view(), name='news_list'),
   path('news/<int:pk>/', ViewNews.as_view(), name='post_detail'),
   path('news/search/', SearchNews.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]