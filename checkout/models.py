from django.db import models

import uuid

from django.contrib.auth.models import User
from products.models import Bikes
from django_countries.fields import CountryField


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
    country = CountryField(blank_label="Country *", null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=(
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ))
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default="")

    def _generate_order_number(self):
        """ Generates an order number """
        return uuid.uuid4().hex.upper()

    def update_grand_total(self):
        """Calculate the grand total of the order including the delivery cost"""
        items = self.order_items.all()
        total_cost = sum(item.subtotal() for item in items)
        delivery_cost = sum(item.calculate_delivery_cost() for item in items)

        self.order_total = total_cost
        self.delivery_cost = delivery_cost
        self.grand_total = total_cost + delivery_cost
        self.save()

        # Update delivery_cost for each OrderItem
        for item in items:
            item.delivery_cost = item.calculate_delivery_cost()
            item.save()

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

    def calculate_delivery_cost(self):
        """Calculates the delivery cost for the bike based on its weight and quantity"""
        total_quantity = self.quantity
        if self.bike.weight > 100:
            delivery_cost = 155 * total_quantity
        elif self.bike.weight > 90:
            delivery_cost = 100 * total_quantity
        else:
            delivery_cost = 90 * total_quantity

        return delivery_cost

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.bike.model} - {self.subtotal()}"
