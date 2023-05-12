from django.shortcuts import render,redirect
from .models import Product_List
from .forms import addStockForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.



# stocks



@method_decorator(login_required,name='dispatch')
class AddStock(View):
    template = 'addStock.html'
    def get(self, request, *args, **kwargs):

        form = addStockForm()
        
        context = { 
                    'form': form,
                    'data': 'Add Stock',
                  }
        
        if request.user.is_superuser:
            return render(request,self.template,context)
        else:
            return render(request,'403error.html',{})

        
    def post(self, request, *args, **kwargs):
                if request.method == 'POST':
                        form = addStockForm(request.POST)
                        if form.is_valid():
                            form.save()
                            messages.success(request, 'Form submission successful')
                            return redirect('addstock')
                        else:
                            messages.warning(request, 'Form submission failed')
                            return redirect('addstock')
                            # print(form.cleaned_data.get('nothing'))
                else:   
                    form = addStockForm()
                    return render(request, self.template)

# UserTable
@method_decorator(login_required,name='dispatch')
class StockTable(View):
    template = 'stocktable.html'
    def get(self, request, *args, **kwargs):

        stockData = Product_List.objects.values()
        form = addStockForm()
        
        i = 0
        context = { 'stockData':stockData,
                    'data': 'Stock Table',
                    'form': form,
                    'id':i}
        if request.user.is_superuser:
            return render(request,self.template,context)
        else:
            return render(request,'404error.html',context)


@method_decorator(login_required,name='dispatch')

class DeleteStock(View):
    def get(self , request, id,*args, **kwargs):
        item = Product_List.objects.get(id=id)
        item.delete()
        return HttpResponseRedirect(reverse('stocktable'))
