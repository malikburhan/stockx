from django.db import models


# Create your models here.
class Sale(models.Model):
    url = models.URLField()
    maximum = models.IntegerField(default=0)
    minimum = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.url}-{self.maximum}-{self.minimum}"