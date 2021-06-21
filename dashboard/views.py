from django.core.files.base import ContentFile
from dashboard.decorators import admin_only, allowed_users, unauthenticated_user
from django.contrib import auth
from django.db.models.query import QuerySet
from dashboard.models import Product
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import CreateCustomerForm, CustomerForm, OrderForm, CreateUserForm, ProductForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# Create your views here.

@login_required(login_url='login')
@admin_only
def home(request):
    print(request.user)
    orders = Order.objects.all()
    customer = Customer.objects.all()

    total_customer = customer.count()
    total_order = orders.count()
    delivered_order = orders.filter(status='Served').count()
    pending_order = orders.filter(status='Pending').count()


    context = {'orders': orders, 'customer': customer,
               'total_customer': total_customer,
               'total_order': total_order, 'delivered_order': delivered_order,
               'pending_order': pending_order,}

    return render(request, 'dashboard/home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()

    context = {'product': products,}

    return render(request, 'dashboard/product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    order = customer.order_set.all()
    order_count = order.count()

    myFilter = OrderFilter(request.GET, queryset=order)
    order = myFilter.qs

    context = {'customer': customer,
               'order': order, 'order_count': order_count, 'filter': myFilter}
    return render(request, 'dashboard/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('Product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        # print('printint post',request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset}

    return render(request, 'dashboard/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('printint post',request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'dashboard/updateForm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form =CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'dashboard/account_setting.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item': order}
    return render(request, 'dashboard/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_order = orders.count()
    delivered_order = orders.filter(status='Served').count()
    pending_order = orders.filter(status='Pending').count()
    print(orders)
    context = {'orders':orders,
               'total_order': total_order, 'delivered_order': delivered_order,
               'pending_order': pending_order}
    return render(request,'dashboard/user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request,pk):
    customer = Customer.objects.get(id = pk)

    form = CreateCustomerForm(instance=customer)

    if request.method == "POST":
        form =CreateCustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'dashboard/updateCustomer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CreateCustomerForm()
    if request.method == "POST":
        form =CreateCustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'dashboard/createCustomer.html',context)



@unauthenticated_user
def register(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,"hello" + " " + username + " " +"Your account has been created")

            return redirect('login')

    context = {'form': form}
    return render(request, 'dashboard/register.html', context)

@unauthenticated_user
def loginUser(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "User name or password is incorrect")

    context = {}

    return render(request, 'dashboard/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
