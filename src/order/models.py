from django.db import models


# Create your models here.
class Sale(models.Model):
    url = models.URLField()
    edit_url = models.URLField()
    purchase = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.url} - {self.edit_url} - {self.purchase}"