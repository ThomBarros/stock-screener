from django.db import models

# Create your models here.
class Screener(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title
    
class Stock(models.Model):
    stock_ticker = models.CharField(max_length=6)
    stock_name = models.TextField()
    recent_price = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return self.stock_ticker