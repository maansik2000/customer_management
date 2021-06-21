from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('product/',views.product,name="product"),
    path('customer/<str:pk_test>',views.customer,name="customer"),
    path('createOrder/<str:pk>/',views.createOrder,name="createOrder"),
    path('updateOrder/<str:pk>/',views.updateOrder,name="updateOrder"),
    path('delete/<str:pk>/',views.deleteOrder,name="deleteOrder"),
    path('register/',views.register,name="register"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('user/',views.userPage,name="user"),
    path('account/',views.accountSettings, name="account"),
    path('createCustomer/',views.createCustomer, name="createCustoemr"),
    path('updateCustomerprofile/<str:pk>/',views.updateCustomer, name="updateCustomer"),
    # path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
