from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User



class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Override the help text for the 'username' field
        self.fields['username'].help_text = None

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        # Override the help text for the 'password' fields
        # Note: UserCreationForm renders 'password' and 'password2'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name')