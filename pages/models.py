# Create your models here.
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from accounts.models import User


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/temp/', null=True)
    time = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=300,default="filename")
    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
@receiver(post_delete, sender=Images)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)