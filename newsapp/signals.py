from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article, User


@receiver(post_save, sender=Article)
def notify_on_publish(sender, instance, created, **kwargs):
    if instance.is_published:
        subscribers = User.objects.filter(
            role="reader", subscribed_journalists=instance.author
        ).distinct()

        recipient_list = [user.email for user in subscribers if user.email]

        if recipient_list:
            send_mail(
                subject=f"New article published: {instance.title}",
                message=f"{instance.author.username} published a new article:\n\n{instance.title}",
                from_email="your_email@gmail.com",
                recipient_list=recipient_list,
                fail_silently=True,
            )
