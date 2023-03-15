from django.db import models

# Create your models here.
class Foods(models.Model):
    product_id = models.IntegerField(primary_key=True)
    merchant_id = models.IntegerField()
    category_id = models.IntegerField()
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
