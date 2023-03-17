from django.db import models

# Create your models here.
class Foods(models.Model):
    product_id = models.IntegerField(primary_key=True)
    merchant_id = models.IntegerField()
    category_id = models.IntegerField()
    ingredients = models.CharField(max_length=255)
    product_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    calories = models.IntegerField()
    product_image = models.CharField(max_length=128)
    stock = models.IntegerField()
    status = models.CharField(max_length=50)
    description = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_product'

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=255)
    middlename = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    weight = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    bmi = models.DecimalField(max_digits=8, decimal_places=2)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'app_users'

class Orders(models.Model):
    order_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    merchant_id = models.IntegerField()
    product_id = models.IntegerField()
    restaurant_id = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    status = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_orders'
