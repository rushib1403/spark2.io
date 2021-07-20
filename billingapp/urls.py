from django.urls import path
from billingapp import views

urlpatterns=[

path('',views.index),
path('register',views.register),

path('register_user',views.register_user),
path('loginpage',views.handlelogin),
path('choose',views.choose),
path('loginnew',views.loginnew),
path('raise',views.raise1),
path('complain',views.complain),
 path('handlerequest/',views.handlerequest),
 path('bill',views.bill),
  path('pay_bill',views.pay_bill),
  path('handlelogout',views.handlelogout),
]