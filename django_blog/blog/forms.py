from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from blog.models import Post, Comment

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm):
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )  # plus password1/password2 from the parent

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        qs = User.objects.filter(username__iexact=username).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").lower()
        if not email:
            return email
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("That email is already in use.")
        return email


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment…"}),
        label="",
    )

    class Meta:
        model = Comment
        fields = ("content",)
