from django.db import models
from store.models import Brand

# Create your models here.
class Requirement(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True)
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  
    size = models.CharField(max_length=55, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to="media/requiremnts/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name