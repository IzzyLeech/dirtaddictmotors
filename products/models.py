from django.db import models


class Bikes(models.Model):
    STROKE_CHOICES = (
        (2, '2-stroke'),
        (4, '4-stroke'),
    )

    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    stroke = models.IntegerField(choices=STROKE_CHOICES)
    engine_capacity = models.DecimalField(max_digits=5, decimal_places=2)
    speed = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    # image
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model}"
