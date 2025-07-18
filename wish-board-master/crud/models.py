from django.db import models

# Create your models here.

class Wish(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=15)
    wish = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.wish}; created at {(self.date)}"