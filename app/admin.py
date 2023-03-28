from django.contrib import admin
from .models import (
    customer,
    product,
    cart,
    OrderPlaced
)

# Register your models here.
@admin.register(customer)
class customerModeladmin(admin.ModelAdmin):
    list_display=[
        'id','name','locality','zipcode','state'
    ]

@admin.register(product)
class productModeladmin(admin.ModelAdmin):
    list_display=[
        'id','title','selling_price','discount_price','discription','brand','catogery','product_image'
    ]

@admin.register(cart)
class cartModeladmin(admin.ModelAdmin):
    list_display=[
        'id','user','product','quantity'
    ]

@admin.register(OrderPlaced)
class cartModeladmin(admin.ModelAdmin):
    list_display=[
        'id','user','product','quantity','customer','orderd_date','staus'
    ]
