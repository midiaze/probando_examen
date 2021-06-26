from apps.login_registro.utils import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request,"index.html")

def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    if request.method == "POST":
        errores = Usuario.objects.validacion_login(request.POST)
        if len(errores)>0:
            context = {
                'errors' : errores,
            }
            return render(request,"login.html", context)
        else:
            usuario = Usuario.objects.get(email=request.POST["email"])
            request.session['id']=usuario.id
            return redirect(f'/dashboard/{usuario.id}')

def registro(request):
    if request.method == "GET":
        return render(request,"registro.html")
    if request.method == "POST":
        errores = Usuario.objects.validacion_registro(request.POST)
        if len(errores)>0:
            context = {
                'errors': errores,
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
                'email': request.POST['email']
            }
            return render(request,"registro.html", context)
        else:
            if len(Usuario.objects.filter(id=1)) == 0:
                user_level = 9
            else:
                user_level = 1
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            usuario_nuevo = Usuario.objects.create(
                first_name=request.POST['first_name'],
                last_name= request.POST['last_name'], 
                email= request.POST['email'], 
                password= hash1,
                user_level = user_level)
            request.session['id']= usuario_nuevo.id
            return redirect(f'/dashboard/{usuario_nuevo.id}')

@login_required
def dashboard(request, id_usuario):    
    context = {
        'usuario': Usuario.objects.get(id=id_usuario),
        'usuarios': Usuario.objects.all()
    }
    return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")
    
