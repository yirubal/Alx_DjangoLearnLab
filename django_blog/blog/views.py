from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.context_processors import messages
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, UpdateView
from rest_framework.reverse import reverse_lazy
from django.contrib import messages
from blog.forms import CustomUserCreationForm, ProfileUpdateForm


# Create your views here.

class RegisterView(CreateView):
    template_name = 'blog/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("blog:login")

    def form_valid(self, form):
        messages.success(self.request, f'Account created for {form.cleaned_data["username"]}')
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "blog/profile.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("blog:profile")

    def get_object(self, queryset=None):
        # This is the magic: the form instance becomes the logged-in user
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated.")
        return super().form_valid(form)


class HomeView(TemplateView):
    template_name = 'blog/home.html'

