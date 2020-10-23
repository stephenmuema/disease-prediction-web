from django.db import models


# Create your models here.
class Files(models.Model):
    name = models.CharField(max_length=500, null=False)
    file = models.FileField(upload_to='csv/', null=True)
    time = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        db_table = "Files"
        verbose_name_plural = "Files"

    # def save(self, *args, **kwargs):
    #     import csv
    #
    #     CSV_PATH = self.file.path
    #     print(CSV_PATH)
    #     # with open(CSV_PATH, newline='') as csvfile:
    #     #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    #     #     for row in spamreader:
    #     #         Record.objects.create(disease=row[1], location=row[4], time=row[0], gender=[3])
    #     super(Files, self).save(*args, **kwargs)


class Record(models.Model):
    disease = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=50, null=False)
    time = models.DateTimeField(null=False)
    gender = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "Records"
        verbose_name_plural = "Records"
