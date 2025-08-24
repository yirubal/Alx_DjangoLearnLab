from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Like, Post, Comment
from notifications.models import Notification

@receiver(post_save, sender=Like)
def notify_post_like(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    actor = instance.user
    recipient = post.author
    if recipient_id := getattr(recipient, "id", None):
        if recipient_id != getattr(actor, "id", None):
            Notification.objects.create(
                recipient=recipient,
                actor=actor,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id,
            )

@receiver(post_save, sender=Comment)
def notify_post_comment(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    actor = instance.author
    recipient = post.author
    if recipient_id := getattr(recipient, "id", None):
        if recipient_id != getattr(actor, "id", None):
            Notification.objects.create(
                recipient=recipient,
                actor=actor,
                verb="commented on your post",
                target_content_type=ContentType.objects.get_for_model(Comment),
                target_object_id=instance.id,
            )
