from django.shortcuts import render,redirect
from app.models import Category,Product,Contact_Us,Order,Brand

from django.contrib.auth import authenticate,login
from app.models import UserCreateForm


from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.http import HttpResponse

from django.contrib.auth.models import User 


def Master(req):
    return render(req,'master.html')

def Index(req):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandid = req.GET.get('brand')
    product = Product.objects.all()
    categoryID = req.GET.get('category')



    if(categoryID):
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif(brandid):
        product = Product.objects.filter(brand = brandid).order_by('-id')
    else:
        product = Product.objects.all()


    context = {
        'category':category,
        'product':product,
        'brand':brand
    }
    return render(req,'index.html',context)


def signup(req):
    if(req.method == 'POST'):
        form = UserCreateForm(req.POST)
        if(form.is_valid()):
            new_user= form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(req,new_user)
            return redirect('index')
    else:
        form = UserCreateForm()
    
    context = {
            'form':form,
    }
    return render(req,'registration/signup.html',context)



def Contact_Page(req):
    if(req.method == 'POST'):
        contact = Contact_Us(
            name = req.POST.get('name'),
            email = req.POST.get('email'),
            subject = req.POST.get('subject'),
            message = req.POST.get('message')
        )
        contact.save()

    return render(req,'contact.html')

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


def Checkout(req):
    if(req.method == "POST"):
        address = req.POST.get('address')
        phone = req.POST.get('phone')
        pincode = req.POST.get('pincode')
        cart = req.session.get('cart')
        uid= req.session.get('_auth_user_id')
        user = User.objects.get(id=uid)

        print(cart)
        for i in cart:
            a=int(cart[i]['price'])
            b=int(cart[i]['quantity'])
            total = a*b
            order = Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                # image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                total = total,
            )
            order.save()
        req.session['cart'] = {}
        return redirect('index')

    return HttpResponse('shreyaaa')
    # return render(req,'checkout.html')

def Your_Order(req):
    uid= req.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    order = Order.objects.filter(user= user)

    context = {
        'order':order
    }


    return render(req,'order.html',context)


def Product_Page(req):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandid = req.GET.get('brand')
    product = Product.objects.all()
    categoryID = req.GET.get('category')

    if(categoryID):
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif(brandid):
        product = Product.objects.filter(brand = brandid).order_by('-id')
    else:
        product = Product.objects.all()
    context = {
        'category':category,
        'brand':brand,
        'product':product,
    }


    return render(req,'product.html',context)


def Product_Detail(req,id):
    # product=Product.objects.filter(id=id).first()
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandid = req.GET.get('brand')
    product = Product.objects.all()
    categoryID = req.GET.get('category')

    if(categoryID):
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif(brandid):
        product = Product.objects.filter(brand = brandid).order_by('-id')
    else:
        product = Product.objects.filter(id=id).first()
    context = {
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(req,'product_detail.html',context)

def Search(req):
    query = req.GET.get('query')
    product = Product.objects.filter(name__icontains = query)
    context = {
        'product':product,
    }

    return render(req,'search.html',context)