from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegisterForm


class RegisterView(View):
    template_name = "users/register.html"
    form_class = RegisterForm

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect(to="app_main:root")
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            messages.success(request, f"Hello {email}! You account has been created!")
            return redirect(to="users:login")
        return render(request, self.template_name, {"form": form})
