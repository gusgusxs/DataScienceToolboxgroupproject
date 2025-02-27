from django import forms
from .models import Cow

class CowForm(forms.ModelForm):
    class Meta:
        model = Cow
        fields = ["name", "breed", "age", "weight", "price", "image", "pedigree_file"]
