from django.shortcuts import get_object_or_404, redirect, render
from .models import Admin_Admission
from demande_admission.models import Demander_Admission
def dashboard(request):
    demandes = Demander_Admission.objects.all()
    username = request.session['username']
    context = {'demandes': demandes,
               'username': username}
    return render(request, 'admins/dashboard.html', context)
def login(request):
    if request.method == "POST":
        username =  request.POST.get('username')
        password = request.POST.get('password')
        user,succ = Admin_Admission.login_user(username=username,password=password)
        if succ:
            request.session['username'] = username
            return redirect('dashboard')
        else :
            context = {'message':'Username or Password is incorrect!'}
            return redirect('login',context=context)
    return render(request, 'admins/login.html')

def detail_demande(request, demande_id):
    demande = get_object_or_404(Demander_Admission, id=demande_id)
    return render(request, 'admins/traite_demande.html', {'demande': demande})
