from django.shortcuts import render
# Create your views here.
from django.shortcuts import render

# Create your views here.
def etape(request):
    
    return render(request, 'informations/etape.html')

def frais(request):
    return render(request, 'informations/fraisadmi.html')