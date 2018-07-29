from django.shortcuts import render,redirect
from .forms import LoginForm ,RegisterForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.utils.http import is_safe_url

def login_page(request):
    form=LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('name')
    next_post = request.POST.get('name')
    print(next_,next_post)
    redirect_path=next_ or next_post or None
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            print("error")
    return render(request,"accounts/login.html",context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context={
        "form":form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        User.objects.create_user(username,email,password)
        return redirect('/login/')
    return render(request,"accounts/register.html",context)

