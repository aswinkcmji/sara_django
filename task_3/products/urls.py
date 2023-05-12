 
from django.urls import path
from . import views

 
urlpatterns = [
	path('addstock', views.AddStock.as_view(), name='addstock'),
	path('stocktable', views.StockTable.as_view(), name='stocktable'),
    path('deletestock/<int:id>/',views.DeleteStock.as_view(),name='deletestock'),



] 
