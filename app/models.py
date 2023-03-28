from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
STATE_CHOICES=(
    ('karnataka','karnataka'),
    ('maharastra','maharastra'),
    ('kerala','kerala'),
    ('madya-pradesh','madya-pradesh'),
    ('west bangal','west bangal'),
    ('goa','goa'),
    ('andra pradesh','andra pradesh'),
    ('sikkim','sikkim'),
    ('Bihar','Bihar')
)
class customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    locality=models.CharField(max_length=100)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)

CATOGORY_CHOICES=(
    ('SH','shoes'),
    ('KU','kurta'),
    ('TW','topware'),
    ('BW','bottomware'),
    ('SR','saree')
)
class product(models.Model):
    title=models.CharField(max_length=200)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    discription=models.TextField()
    brand=models.CharField(max_length=100)
    catogery=models.CharField(choices=CATOGORY_CHOICES,max_length=10)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity* self.product.discount_price

STATUS_CHOICES=(
    ('accepted','accepted'),
    ('packed','packed'),
    ('on the way','on the way'),
    ('Deliverd','Deliverd'),
    ('cancel','cancel')
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    customer=models.ForeignKey(customer,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    orderd_date=models.DateTimeField(auto_now_add=True)
    staus=models.CharField(choices=STATUS_CHOICES,default='pending',max_length=50)

    @property
    def total_cost(self):
        return self.quantity* self.product.discount_price

