# connecting userSide with views

from django.urls import path
from . import views
from adminPanel.views import History, HomePage,Billing,Table,AddUser
urlpatterns = [
    path("", views.Home.as_view(), name = "user_hom"),
    path("shop/", views.Shop.as_view(), name = "user_shop"),
    path("home/",HomePage.as_view(), name = "user_home"),
    path("billing/",Billing.as_view(), name = "user_billing"),
    path("table/",Table.as_view(), name = "user_table"),
    path("notifications/",History.as_view(), name = "user_history"),
    path("checkout/<int:id>",views.Checkout.as_view(), name = "checkout"),
    path('register/',views.Register.as_view(),name='register'),
   path('adduser/',AddUser.as_view(),name='user_adduser'),
]