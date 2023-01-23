from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from .forms import PostForm
from .models import Post, Category
from django.http import HttpResponse, HttpResponseRedirect
from .filters import NewsFilter
from django.shortcuts import redirect, get_object_or_404, render


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

    # def post(self, request, **kwargs):
    #     user = request.user
    #
    #     if 'subscribe' in request.POST:
    #         category = Category.objects.get(id=request.POST['subscribe'])
    #         category.subscribes.add(user)
    #         self.cate_id = request.POST['subscribe']
    #         print(self.cate_id, 'sub')
    #     elif 'unsubscribe' in request.POST:
    #         category = Category.objects.get(id=request.POST['unsubscribe'])
    #         category.subscribes.remove(user)
    #         self.cate_id = request.POST['unsubscribe']
    #         print(self.cate_id, 'unsub')
    #     return HttpResponseRedirect('')

    # def get_context_data(self, **kwargs):
    #     # def f(request):
    #     #     if 'subscribe' in request.POST:
    #     #         self.cate_id = request.POST['subscribe']
    #     #         return self.cate_id
    #     #     elif 'unsubscribe' in request.POST:
    #     #         self.cate_id = request.POST['unsubscribe']
    #     #         return self.cate_id
    #
    #
    #     context = super().get_context_data(**kwargs)
    #     # print(self.cate_id, 'context')
    #     self.post_category = Post.objects.get(id=self.kwargs['pk']).post_category.get(id=category.id)
    #     context['is_not_subscriber'] = self.request.user not in self.post_category.subscribes.all()
    #     # context[f'category{cat_id.id}'] = self.post_category
    #
    #
    #     return context
    #



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

    def post(self, request, *args, **kwargs):
        send_mail(
            subject='Test',
            # имя клиента и дата записи будут в теме для удобства
            message='Post.post_text',  # сообщение с кратким описанием проблемы
            from_email='posholokia@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['ilya.posholokk@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        return redirect('news_list')


class CategoryList(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_list_view'

    def get_queryset(self):
        self.post_category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.post_category).order_by('-post_date')
        print(self.post_category, self.kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.post_category.subscribes.all()
        context['category'] = self.post_category
        return context


def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribes.add(user)
    print()
    message = 'Вы успешно подписались'
    return render(request, 'news/subscribe.html', {'post_category': category, 'message': message})



