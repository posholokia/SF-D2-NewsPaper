from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver # импортируем нужный декоратор
from NewsPaper import settings
from .models import PostCategory, Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_mail_post(post_text, pk, title, subscribers):
    for sub in subscribers:
        html_content = render_to_string(
            'news/send_mail_post.html',
            {
                'text': post_text[:49],
                'username': sub.username,
                'link': f'{settings.SITE_URL}/news/{pk}'
            }
        )
    
        msg = EmailMultiAlternatives(
            subject=f'{title}',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.email],
            )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

   
# @receiver(m2m_changed, sender=PostCategory)
# def notify_managers_appointment(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         subscribers = []  # список подписчиков
#         categories = instance.post_category.all()
#         for category in categories:
#             subscribers += category.subscribers.all()  # заполняем подписчиками категории
#             # удаляем дублирование подписчиков, когда юзер подписан на несколько категорий,
#             # присвоенных созданной статье, чтобы не дублировать отправку писем
#             subscribers = list(set(subscribers))
#
#         send_mail_post(instance.post_text, instance.pk, instance.post_title, subscribers)
       
       
# @receiver(pre_save, sender=Post)
# def daily(sender, *args, **kwargs):
#     print('sender: ', sender, '\nargs:', args, '\nkwargs: ', kwargs)
#     print(kwargs['instance'].post_author)
#     author = kwargs['instance'].post_author
#     today = datetime.date.today()
#     a = Post.objects.filter(post_author=author, post_date__gte=today).all()
#     if a > 3:
#         print(len(a))
    
    
