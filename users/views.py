import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import EmailOTP
from .forms import SignupForm, OTPVerifyForm

User = get_user_model()


def signup_view(request):
    """Step 1: collect email + password, send OTP."""
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            EmailOTP.objects.filter(email=email).delete()

            otp_obj = EmailOTP.objects.create(
                email=email,
                password_hash=make_password(password),
            )

            _send_otp_email(email, otp_obj.otp)

            request.session["otp_email"] = email
            messages.success(
                request,
                f"A 6-digit verification code has been sent to {email}.",
            )
            return redirect("users:verify_otp")
    else:
        form = SignupForm()

    return render(request, "users/signup.html", {"form": form})


def verify_otp_view(request):
    """Step 2: user enters OTP, account gets created."""
    email = request.session.get("otp_email")
    if not email:
        messages.error(request, "Session expired. Please sign up again.")
        return redirect("users:signup")

    try:
        otp_obj = EmailOTP.objects.get(email=email)
    except EmailOTP.DoesNotExist:
        messages.error(request, "No pending verification found. Please sign up again.")
        return redirect("users:signup")

    if request.method == "POST":
        if "resend" in request.POST:
            if otp_obj.is_expired():
                EmailOTP.objects.filter(email=email).delete()
                messages.error(request, "Code expired. Please sign up again.")
                return redirect("users:signup")
            otp_obj.otp = _make_otp()
            otp_obj.attempts = 0
            otp_obj.expires_at = timezone.now() + timedelta(minutes=10)
            otp_obj.save()
            _send_otp_email(email, otp_obj.otp)
            messages.success(request, "A new code has been sent.")
            return redirect("users:verify_otp")

        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered = form.cleaned_data["otp"]

            if otp_obj.is_locked():
                messages.error(request, "Too many wrong attempts. Please sign up again.")
                otp_obj.delete()
                return redirect("users:signup")

            if otp_obj.is_expired():
                otp_obj.delete()
                messages.error(request, "The code has expired. Please sign up again.")
                return redirect("users:signup")

            if entered != otp_obj.otp:
                otp_obj.attempts += 1
                otp_obj.save()
                remaining = 5 - otp_obj.attempts
                form.add_error("otp", f"Wrong code. {remaining} attempt(s) left.")
            else:
                user = User.objects.create(
                    email=email,
                    username=email,
                    password=otp_obj.password_hash,
                    is_active=True,
                )
                otp_obj.delete()
                del request.session["otp_email"]
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                messages.success(request, "Account created! Welcome to UrbanCase.")
                return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = OTPVerifyForm()

    total_secs = max(0, (otp_obj.expires_at - timezone.now()).total_seconds())
    minutes_left = int(total_secs // 60)
    secs_left = int(total_secs % 60)

    return render(
        request,
        "users/verify_otp.html",
        {
            "form": form,
            "email": email,
            "minutes_left": minutes_left,
            "secs_left": secs_left,
            "total_secs": int(total_secs),
        },
    )


def _make_otp():
    return "".join(random.choices(string.digits, k=6))


def _send_otp_email(email, otp):
    send_mail(
        subject="Your UrbanCase verification code",
        message=(
            f"Your one-time verification code is: {otp}\n\n"
            "This code is valid for 10 minutes.\n"
            "Do not share this code with anyone."
        ),
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@urbancase.com"),
        recipient_list=[email],
        fail_silently=False,
    )
