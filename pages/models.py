# Create your models here.
from django.db import models
from django.utils.safestring import mark_safe

from accounts.models import User


class Images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/temp/', null=True)
    time = models.DateTimeField(auto_now_add=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True