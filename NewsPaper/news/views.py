from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post, Category, Author
from .filters import NewsFilter
from django.shortcuts import get_object_or_404, render, redirect
import datetime


class NewsList(ListView):
    model = Post
    ordering = '-post_date'
    template_name = 'news/news.html'
    context_object_name = 'news'
    paginate_by = 10
    

class ViewNews(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
    

class SearchNews(ListView):
    model = Post
    template_name = 'news/search_news.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.update_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('news_list')


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'news/post_create.html'

    # Ограничение на количетво новостей в сутки
    def form_valid(self, form):
        user_name = self.request.user  # получаем текущего юзера
        author_name = Author.objects.get(author=user_name)  # получаем модель автора текущего юзера
        today = datetime.date.today()
        # получаем QueryDict всех статей автора за сегодня
        number_of_posts = Post.objects.filter(post_author=author_name, post_date__gte=today).all()
        if len(number_of_posts) > 3:  # если статей больше 3, отправляем на страницу с информацией об ошибке
            return redirect('post_limit')
        else:  # иначе сохраняем в БД
            form = PostForm(self.request.POST)  # получаем значения полей fields из формы
            post = form.save(commit=False)  # форму нужно дополнить автором
            post.post_author = author_name  # post_author - залогиненый автор
            post.save()
            return super().form_valid(form)

    
class AllCategoriesList(ListView):
    model = Category
    template_name = 'news/all_categories.html'
    context_object_name = 'all_categories_view'


class CategoryList(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_list_view'

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-post_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribers.all()
        context['category'] = self.post_category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if user not in category.subscribers.all():
        category.subscribers.add(user)
        message = 'Вы успешно подписались'
    else:
        category.subscribers.remove(user)
        message = 'Подписка отменена'
    return render(request, 'news/subscribe.html', {'post_category': category, 'message': message})


def post_limit(request):
    return render(request, 'news/post_limit.html')
