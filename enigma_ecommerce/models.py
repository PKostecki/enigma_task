from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime, timedelta


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images")
    image_thumbnail = models.ImageField(upload_to="product_images_thumbnails")

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.image_thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        if self.image:
            img = Image.open(self.image.path)
            img.thumbnail((200, 200))
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG')
            thumbnail = InMemoryUploadedFile(thumb_io, None, f'{self.image.name.split(".")[0]}_thumbnail.jpg',
                                             'image/jpeg', thumb_io.tell, None)
            self.image_thumbnail.save(thumbnail.name, thumbnail, save=False)
            super().save(update_fields=['image_thumbnail'])


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.TextField(max_length=255)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateField(auto_now_add=True)
    payment_due_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order: {self.pk} for {self.customer.username}"

    def save(self, *args, **kwargs):
        if not self.payment_due_date:
            self.payment_due_date = datetime.now().date() + timedelta(days=5)

        super().save(*args, **kwargs)

        if not self.total_price:
            total_price = sum(item.product.price * item.quantity for item in self.orderitem_set.all())
            self.total_price = total_price

        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} for {self.product} in Order: {self.order.pk}"
