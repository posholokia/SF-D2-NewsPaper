from celery import shared_task
from NewsPaper import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime
from news.models import Post, Category


@shared_task
def send_mail_post(post_text, pk, title, username, email):
    html_content = render_to_string(
        'news/send_mail_post.html',
        {
            'text': post_text[:49],
            'username': username,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    
    msg = EmailMultiAlternatives(
        subject=f'{title}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()



@shared_task
def weekly_send_mail():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(post_date__gte=last_week)
    categories = set(posts.values_list('post_category__name', flat=True))
    subscribes = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'news/weekly_post.html',
        {
            'posts': posts,
            'link': settings.SITE_URL
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribes,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    