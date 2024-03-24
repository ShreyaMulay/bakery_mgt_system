from django.shortcuts import render,redirect
from app.models import Category,Product,Contact_Us,Order,Brand,OrderNew,OrderItem

from django.contrib.auth import authenticate,login
from app.models import UserCreateForm


from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.http import HttpResponse

from django.contrib.auth.models import User 

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt


import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))


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
    print("::shreya",product)
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
    # if(req.method == "POST"):
    #     address = req.POST.get('address')
    #     phone = req.POST.get('phone')
    #     pincode = req.POST.get('pincode')
    #     cart = req.session.get('cart')
    #     uid= req.session.get('_auth_user_id')
    #     user = User.objects.get(id=uid)

    #     print(cart)
    #     for i in cart:
    #         a=int(cart[i]['price'])
    #         b=int(cart[i]['quantity'])
    #         total = a*b
    #         order = Order(
    #             user = user,
    #             product = cart[i]['name'],
    #             price = cart[i]['price'],
    #             quantity = cart[i]['quantity'],
    #             image = cart[i]['image'],
    #             address = address,
    #             phone = phone,
    #             pincode = pincode,
    #             total = total,
    #         )
    #         order.save()
    #     req.session['cart'] = {}
    #     return redirect('index')

    # # return HttpResponse('shreyaaa')
    # return render(req,'checkout.html')

    amount_str = req.POST.get('amount')
    amount_float = float(amount_str)
    amount = int(amount_float)



    print("::amount",amount)
    payment = client.order.create({
        "amount":amount,
        "currency":"INR",
        "payment_capture":"1"
    })

    print("::payment",payment)

    order_id = payment['id']

    context = {
        "order_id":order_id,
        "payment":payment
    }
    return render(req,'checkout.html',context)

def Your_Order(req):
    uid= req.session.get('_auth_user_id')
    user = User.objects.get(id=uid)

    order = OrderItem.objects.filter(user = user)

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
    product1 = Product.objects.all()

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
        'product1':product1,
    }

    return render(req,'product_detail.html',context)

def Search(req):
    query = req.GET.get('query')
    product = Product.objects.filter(name__icontains = query)
    context = {
        'product':product,
    }

    return render(req,'search.html',context)

def Place_Order(req):
    if req.method == 'POST':
        uid= req.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = req.session.get('cart')

        name = req.POST.get('name')
        country = req.POST.get('country')
        paymentmode = req.POST.get('paymentmode')
        address = req.POST.get('address')
        city = req.POST.get('city')
        state = req.POST.get('state')
        postcode = req.POST.get('postcode')
        phone = req.POST.get('phone')
        email = req.POST.get('email')
        order_id = req.POST.get('order_id')
        payment = req.POST.get('payment')
        amount = req.POST.get('amount')


        # print(order_id,payment,name,address,country,city,state,postcode,phone,email)

        context = {
            "order_id": order_id,
            "paymentmode": paymentmode
        }

        order = OrderNew(
            user=user,
            name=name,
            country=country,
            paymentmode= paymentmode,
            address=address,
            city = city,
            state = state,
            postcode = postcode,
            phone = phone,
            email = email,
            payment_id = order_id,
            amount = amount
        )
        order.save()

        print("::paymentmode",paymentmode)
        for i in cart:
            a=int(cart[i]['price'])
            b=int(cart[i]['quantity'])
            total = a*b

            item = OrderItem(
                user = user,
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()

        return render(req,'placeorder.html',context)

@csrf_exempt
def Success(req):
    print("::inside success function")
    if req.method == 'POST':
        a = req.POST
        order_id = ""
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break

        user = OrderNew.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
        req.session['cart'] = {}
    else:
        req.session['cart'] = {}
    return render(req,'thank-you.html')