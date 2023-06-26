from django.db import models

import uuid

from django.contrib.auth.models import User
from products.models import Bikes


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    postcode = models.CharField(max_length=40, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    county = models.CharField(max_length=80, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=(
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ))
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _generate_order_number(self):
        """ Generates an order number """
        return uuid.uuid4().hex.upper()

    def update_grand_total(self):
        """ Calculate the grand total of the order """
        items = self.order_items.all()
        total_cost = sum(item.subtotal() for item in items)
        delivery_cost = self.calculate_delivery_cost(items)
        grand_total = total_cost + delivery_cost

        self.order_total = total_cost
        self.delivery_cost = delivery_cost
        self.grand_total = grand_total
        self.save()

    def calculate_delivery_cost(self, items):
        """Calculates the delivery cost of the delivery based on the weight of bikes"""
        total_weight = sum(item.bike.weight for item in items)
        if total_weight > 100:
            return 155
        elif total_weight > 90:
            return 100
        else:
            return 90

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    bike = models.ForeignKey(Bikes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.bike.model} - {self.subtotal()}"
