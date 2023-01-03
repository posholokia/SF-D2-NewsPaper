from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import PostForm
from .models import Post
from django.http import HttpResponse
from .filters import NewsFilter


class NewsList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 1


class ViewNews(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'


class SearchNews(ListView):
    model = Post
    template_name = 'news/search_news.html'
    context_object_name = 'news'

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
