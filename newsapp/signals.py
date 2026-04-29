from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article, User


@receiver(post_save, sender=Article)
def notify_on_publish(sender, instance, created, **kwargs):
    if instance.is_published:
        # Use the journalist author if available.
        # If the article was created by an editor, use the editor instead.
        creator = instance.author if instance.author else instance.editor
        creator_name = creator.username if creator else "Unknown user"

        subscribers = User.objects.filter(
            role="reader",
            subscribed_journalists=instance.author
        ).distinct()

        recipient_list = [user.email for user in subscribers if user.email]

        if recipient_list:
            send_mail(
                subject=f"New article published: {instance.title}",
                message=f"{creator_name} published a new article:\n\n{instance.title}",
                from_email="your_email@gmail.com",
                recipient_list=recipient_list,
                fail_silently=True,
        )