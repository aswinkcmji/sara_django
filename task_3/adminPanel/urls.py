from django.urls import path
from . import views


urlpatterns = [
    # path('',views.LoginPage.as_view(),name='login'),
    path('home/',views.HomePage.as_view(),name='home'),
    path('logout/',views.logout,name='logout'),
    path('table/',views.Table.as_view(),name='table'),
    path('billing/',views.Billing.as_view(),name='billing'),
    path('history/',views.History.as_view(),name='history'),
    path('adduser/',views.AddUser.as_view(),name='adduser'),
    path('usertable/',views.UserTable.as_view(),name='usertable'),
    path('updateuser/<int:id>/',views.UpdateUser.as_view(),name='updateuser'),
    path('bonustable/',views.Bonuslist.as_view(),name='bonustable'),
]

