from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError

User = get_user_model()


class SignupForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "placeholder": "you@example.com",
            "class": "form-control form-control-lg rounded-3",
            "autocomplete": "email",
        })
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Min. 8 characters",
            "class": "form-control form-control-lg rounded-3",
            "autocomplete": "new-password",
        }),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Repeat your password",
            "class": "form-control form-control-lg rounded-3",
            "autocomplete": "new-password",
        }),
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1", "")
        p2 = self.cleaned_data.get("password2", "")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Passwords do not match.")
        return p2

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1", "")
        if p1:
            try:
                password_validation.validate_password(p1)
            except ValidationError as e:
                self.add_error("password1", e)
        return cleaned


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter 6-digit code",
            "class": "form-control form-control-lg rounded-3 text-center letter-spacing-otp",
            "maxlength": "6",
            "inputmode": "numeric",
            "pattern": "[0-9]{6}",
            "autocomplete": "one-time-code",
        }),
    )

    def clean_otp(self):
        val = self.cleaned_data["otp"].strip()
        if not val.isdigit():
            raise ValidationError("OTP must be 6 digits.")
        return val
