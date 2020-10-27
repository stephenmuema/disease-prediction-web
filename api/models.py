from django.db import models

# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Files(models.Model):
    name = models.CharField(max_length=500, null=False)
    file = models.FileField(upload_to='csv/', null=True)
    time = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        db_table = "Files"
        verbose_name_plural = "Files"


@receiver(post_delete, sender=Files)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
