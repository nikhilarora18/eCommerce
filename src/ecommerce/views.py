from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import ContactForm, LoginForm, RegisterForm


# User=get_user_model()

def home(request):
    context = {
        "title": "Hello world",
        "content": "Welcome to the homepage"
    }
    return render(request, "home.html", context)


def about(request):
    context = {
        "title": "About Page",
        "content": "Welcome to the about page"
    }
    return render(request, "home.html", context)


def contact(request):
    contactform = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page",
        "content": "Welcome to the contact page",
        "form": contactform
    }
    if contactform.is_valid():
        print(contactform.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thankyou for your submission"})

    if contactform.errors:
        errors = contactform.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, "contact/view.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print("User logged in")
    print(request.user.is_authenticated)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        # print(user)
        # print(request.user.is_authenticated)
        if user is not None:
            print(request.user.is_authenticated)
            login(request, user)
            # context['form']=LoginForm()
            return redirect("/")
        else:
            print("error")
    return render(request, "auth/login.html", context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        User.objects.create_user(username, email, password)
        # print(new_user)
    return render(request, "auth/register.html", context)
