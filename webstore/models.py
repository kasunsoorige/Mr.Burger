from django.db import models
import json

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    price = models.FloatField()
    img_url = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Order(models.Model):
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
