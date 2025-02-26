from django import forms
from .models import FarmProfile

class FarmProfileForm(forms.ModelForm):
    class Meta:
        model = FarmProfile
        fields = ["farm_name", "location", "phone", "description"]
