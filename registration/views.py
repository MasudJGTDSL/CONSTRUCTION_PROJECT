from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Accounts.decorators import admin_only, allowed_users, unauthenticated_user

# Create your views here.
from .models import *
from django.contrib.auth.models import Group, User
from .forms import CreateUserForm


@login_required
@allowed_users(allowed_roles=["Admin"])
def registerPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            u = User.objects.get(username=request.POST["username"])
            u.groups.set(
                [
                    form.cleaned_data.get("group"),
                ]
            )
            u.save()
            user = form.cleaned_data.get("username")
            messages.success(request, f"Account has created for {user}")

            return redirect("./")

    context = {"form": form}
    return render(request, "registration/register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, "You have successfully logged in!")
                return redirect("/")
            else:
                messages.info(request, "Username OR password is incorrect")

        context = {}
        return render(request, "registration/login.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, "You have successfully logged out!")
    return redirect("/registration/loginPage")


@login_required(login_url="login")
def index(request):
    return render(request, "accounts/dashboard.html")
