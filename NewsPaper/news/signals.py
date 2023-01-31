from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_mail_post

        
@receiver(m2m_changed, sender=PostCategory)
def notify_managers_appointment(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers = []  # список подписчиков
        categories = instance.post_category.all()
        for category in categories:
            subscribers += category.subscribers.all()  # заполняем подписчиками категории
            # удаляем дублирование подписчиков, когда юзер подписан на несколько категорий,
        # присвоенных созданной статье, чтобы не дублировать отправку писем
        subscribers = list(set(subscribers))
        for sub in subscribers:
            username = str(sub.username)  # письма будут персонализированы
            email = [sub.email]
            send_mail_post.apply_async((instance.post_text, instance.pk, instance.post_title, username, email))

       

    
