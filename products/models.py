from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from cloudinary.models import CloudinaryField


class Bikes(models.Model):
    STROKE_CHOICES = (
        (2, '2-stroke'),
        (4, '4-stroke'),
    )

    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(2100)
        ], default=2024
    )
    stroke = models.IntegerField(choices=STROKE_CHOICES)
    engine_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    speed = models.IntegerField()
    weight = models.DecimalField(max_digits=8, decimal_places=2, default=90)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    sku = models.CharField(max_length=254, null=True, blank=True)
    image = CloudinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['manufacturer']

    def __str__(self):
        return f"{self.manufacturer} {self.model} {self.engine_capacity}"
