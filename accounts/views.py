from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    UserUpdateForm,
    ProfileUpdateForm,
    NoteForm
)

from .models import Note


# Register
def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# Login
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect(
                "dashboard"
            )

        else:

            messages.error(
                request,
                "Invalid username/password"
            )

    return render(
        request,
        "login.html"
    )


# Logout
def user_logout(request):

    logout(request)

    return redirect(
        "login"
    )


# Profile edit
@login_required
def profile(request):

    if request.method == "POST":

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():

            user_form.save()
            profile_form.save()

            return redirect(
                "profile"
            )

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileUpdateForm(
            instance=request.user.profile
        )

    return render(
        request,
        "profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form
        }
    )


# Dashboard with notes
@login_required
def dashboard(request):

    notes = Note.objects.filter(
        user=request.user
    )

    if request.method == "POST":

        form = NoteForm(
            request.POST
        )

        if form.is_valid():

            note = form.save(
                commit=False
            )

            note.user = request.user

            note.save()

            return redirect(
                "dashboard"
            )

    else:

        form = NoteForm()

    return render(
        request,
        "dashboard.html",
        {
            "notes": notes,
            "form": form
        }
    )