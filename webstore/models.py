from django.db import models
import json
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Import the User model
from django.db import models
from django.conf import settings


# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    img_url = models.ImageField(upload_to='static/')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Allow null values
        blank=True,  # Allow blank values in forms
    ) # Link order to user
    items = models.TextField()  # Use for sqlite
    # items = models.JSONField()  # Uncomment for MySQL to store cart items in JSON format
    order_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Incomplete', 'Incomplete'),
        ('Complete', 'Complete'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Incomplete')
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    





    # To save the items as JSON for SQLite (only needed if using SQLite)
    def save(self, *args, **kwargs):
        if isinstance(self.items, dict):
            self.items = json.dumps(self.items)  # Convert dictionary to JSON string
        super().save(*args, **kwargs)

    # To load items as a dictionary when needed
    def get_items(self):
        return json.loads(self.items)


class ShippingDetails(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)  # Link to Order
    name = models.CharField(max_length=255)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    house_no = models.CharField(max_length=10)
    street1 = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Shipping for Order #{self.order.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"

    # Calculate the total price for an individual item (price * quantity)
    @property
    def total_price(self):
        return self.item.price * self.quantity





class Reservation(models.Model):
    date = models.DateField()
    time = models.TimeField()
    num_people = models.IntegerField()
    space_preference = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)


class Notification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for Order #{self.order.id}"

# Signal to create a notification when a new order is placed
@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            order=instance,
            message=f"New Order Received: Order #{instance.id}"
        )