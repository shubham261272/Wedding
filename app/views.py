
from django.views.generic import ListView
from django.shortcuts import render,redirect
from django.views import View
from .models import (
    customer,
    product,
    cart,
    OrderPlaced
)
from .forms import customeRegistrationClass,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')

class productView(View):
    def get(self,request):
        topwear=product.objects.filter(catogery='TW')
        bottomwear=product.objects.filter(catogery='BW')
        shoes=product.objects.filter(catogery='SH')
        kurta=product.objects.filter(catogery='KU')
        saree=product.objects.filter(catogery='SR')
        return render(request, 'app/home.html',
        {'topwear':topwear,
        'bottomwear':bottomwear,
        'shoes':shoes,
        'kurta':kurta,
        'saree':saree
        })

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class productdetailView(View):
    def get(self,request,pk):
        pro=product.objects.get(pk=pk)
        product_in_cart=False
        if request.user.is_authenticated:
           product_in_cart=cart.objects.filter(Q(product=pro.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'pro':pro,'pic':product_in_cart})
 
def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      crt=cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      crt.quantity+=1
      crt.save()
      amount=0.0
      shipping_amount=70.0
      cart_product=[p for p in cart.objects.all() if p.user == request.user]
      for p in cart_product:
            amount1=(p.quantity * p.product.discount_price)
            amount += amount1
      data={'quantity':crt.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount
            }
      return JsonResponse(data) 
 
def minus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      crt=cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      crt.quantity-=1
      crt.save()
      amount=0.0
      shipping_amount=70.0
      cart_product=[p for p in cart.objects.all() if p.user == request.user]
      for p in cart_product:
            amount1=(p.quantity * p.product.discount_price)
            amount += amount1
      data1={'quantity':crt.quantity,
            'amount': amount,
            'totalamount':amount+shipping_amount
            }
      return JsonResponse(data1) 

@login_required
def add_to_cart(request):
 user=request.user
 prod=request.GET.get('prod_id')
 prod1=product.objects.get(id=prod)
 cart(user=user,product=prod1).save()
 return redirect('/cart')

@login_required
def show_cart(request):
   if request.user.is_authenticated:
      user=request.user
      carts=cart.objects.filter(user=user)
      amount=0.0
      shipping_amount=70.0
      total_amount=0.0
      cart_product=[p for p in cart.objects.all() if p.user == user]
      if cart_product:
         for p in cart_product:
            amount1=(p.quantity * p.product.discount_price)
            amount += amount1
            totalamount= amount + shipping_amount
         return render(request,'app/addtocart.html',{'carts':carts,'amount':amount,'totalamount':totalamount})
      else:
         return render(request,'app/emptycart.html')

     
def remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      crt=cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      crt.delete()
      amount=0.0
      shipping_amount=70.0
      cart_product=[p for p in cart.objects.all() if p.user == request.user]
      for p in cart_product:
            amount1=(p.quantity * p.product.discount_price)
            amount += amount1
      data={
            'amount': amount,
            'totalamount':amount + shipping_amount
            }
      return JsonResponse(data) 
         

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request): 
 return render(request, 'app/profile.html')

def address(request):
 add=customer.objects.filter(user=request.user)
 return render(request,'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 order_placed=OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'ops':order_placed})


def kurta(request,data=None):
    if data == None:
        kurta=product.objects.filter(catogery='KU')
    elif data=='zara' or data=='zeel' or data=='ahara':
        kurta=product.objects.filter(catogery='KU').filter(brand=data)
    elif data=='below':
        kurta=product.objects.filter(catogery='KU').filter(discount_price__lt=10000)
    elif data=='above':
        kurta=product.objects.filter(catogery='KU').filter(discount_price__gt=10000)
    return render(request, 'app/kurta.html',{'kurta':kurta})

def login(request):
 return render(request,'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class customerregistrationView(View):
    def get(self,request):
        form=customeRegistrationClass()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=customeRegistrationClass(request.POST)
        if request.method=='POST':
            if form.is_valid():
                messages.success(request,'Congratulations!! registerd successfully')
                form.save()
        return render(request, 'app/customerregistration.html',{'form':form})

  
def checkout(request):
 user=request.user
 add=customer.objects.filter(user=user)
 cart_item=cart.objects.filter(user=user)
 amount=0.0
 shipping_amount=70.0
 totalamount=0
 cart_product=[p for p in cart.objects.all() if p.user==request.user]
 if cart_product:
    for p in cart_product:
       temp_amount=(p.quantity*p.product.discount_price)
       amount+=temp_amount
    totalamount=amount+shipping_amount
 return render(request,'app/checkout.html',{'add':add,'cart_item':cart_item,'totalamount':totalamount})

@method_decorator(login_required,name='dispatch')
class profileView(View):
   def get(self,request):
      form=CustomerProfileForm()
      return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
   def post(self,request):
      form=CustomerProfileForm(request.POST)
      if form.is_valid():
         usr=request.user
         name=form.cleaned_data['name']
         locality=form.cleaned_data['locality']
         city=form.cleaned_data['city']
         state=form.cleaned_data['state']
         zipcode=form.cleaned_data['zipcode']
         reg=customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
         reg.save()
         messages.success(request,'Congratulation!! profile Updated Successfully')
         return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
 
def payment_done(request):
   custid=request.GET.get('custid')
   user=request.user
   customer1=customer.objects.get(id=custid)
   crt=cart.objects.filter(user=user)
   for ct in crt:
      OrderPlaced(user=user,customer=customer1,product=ct.product,quantity=ct.quantity).save()
      ct.delete()
   return redirect("orders")

class SearchResultsView(ListView):
    model = product
    template_name = 'app/search.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('search')
        products=product.objects.filter(Q(title__icontains=query))
        return products
     
         
      
        
    
