from django import forms
from .models import *


class yacht_detailsForm(forms.ModelForm):
    class Meta:
        model   = yacht_details
        fields  = (
            "yacht_type",
            "yacht_sizes",
            "yacht_style_categories",
            "rent_price",
            "yacht_image"
        )
