import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Order


def validate_phone(value):
    cleaned = re.sub(r"[\s\-\(\)\+]", "", value)
    if not re.match(r"^\d{7,15}$", cleaned):
        raise ValidationError("Enter a valid phone number (7 to 15 digits).")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["customer_name", "customer_phone", "customer_address", "quantity"]
        widgets = {
            "customer_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "customer_phone": forms.TextInput(attrs={"placeholder": "+91 98765 43210"}),
            "customer_address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Delivery address"}
            ),
            "quantity": forms.NumberInput(attrs={"min": 1, "max": 99}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer_phone"].validators.append(validate_phone)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")