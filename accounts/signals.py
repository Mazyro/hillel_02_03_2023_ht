from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_user(created, **kwargs):
    instance = kwargs['instance']
    if created:
        # Используем имя из username для First Name
        instance.first_name = instance.username
        # Задаем "No surname yet" для Last Name
        instance.last_name = 'No surname yet'
        instance.save()
    else:
        pass
