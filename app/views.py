from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

from .forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order
from django.shortcuts import get_object_or_404


# Create your views here.


def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'app/index.html', {'cat_list': cat_list})
    # cat_list = Category.objects.all().order_by('id')[:10]
    # response = HttpResponse()
    # heading1 = '<p>' + 'List of categories: ' + '</p>'
    # response.write(heading1)
    # for category in cat_list:
    #     para = '<p>'+ str(category.id) + ': ' + str(category) + '</p>'
    #     response.write(para)
    #
    # product_list = Product.objects.all().order_by('-price')[:5]
    # heading2 = '<p>' + 'List of products: ' + '</p>'
    # response.write(heading2)
    # for product in product_list:
    #     para = '<p>' + str(product.name) + ': ' + str(product.price) + '</p>'
    #     response.write(para)
    #
    # return response


def about(request):
    # response = HttpResponse()
    # para = '<h2> This is an Online Store APP. </h2>'
    # response.write(para)
    # return response
    return render(request, 'app/about.html')


def detail(request, cat_no):
    response = HttpResponse()
    # category = get_object_or_404(Category, name=cat_no)
    # product_list = Product.objects.filter(category=category)
    # get_object_or_404()

    # heading1 = '<H2>' + 'Category ' + cat_no + '</H2><br>'
    # response.write(heading1)
    # heading2 = '<H2>' + 'Warehouse ' + category.warehouse + '</H2>'
    # response.write(heading2)
    # product_list = Product.objects.filter(category=category)
    # for product in product_list:
    #     para = '<p>' + str(product.name) + '</p>'
    #     response.write(para)
    #
    # return response

    category = get_object_or_404(Category, name=cat_no)
    product_list = Product.objects.filter(category=category)
    return render(request, 'app/detail.html',
                  {'cat_no': cat_no,
                   'category': category,
                   'product_list': product_list})


def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'app/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                Product.objects.filter(id=order.product.id).update(stock = (order.product.stock - order.num_units))
                order.save()
                msg = 'Your order has been placed successfully.'
                return render(request, 'app/order_response.html', {'msg': msg})
            else:
                msg = 'We do not have sufficient stock to fill your order.'
                return render(request, 'app/order_response.html', {'msg': msg})

    else:
        form = OrderForm()
        return render(request, 'app/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    product = Product.objects.get(id=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                Product.objects.filter(id=product.id).update(interested=(product.interested + 1))
                cat_list = Category.objects.all().order_by('id')[:10]
                return render(request, 'app/index.html', {'cat_list': cat_list})

    else:
        if product.stock == 0:
            msg = "Product out of stock"
        else:
            msg = ''
        form = InterestForm()
        return render(request, 'app/productdetail.html', {'form': form,
                                                          'name': product.name,
                                                          'interested': product.interested,
                                                          'price': product.price,
                                                          'msg': msg})

