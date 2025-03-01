from django import forms
from .models import Cow

class CowForm(forms.ModelForm):
    age = forms.IntegerField(min_value=0)  # ✅ ห้ามอายุติดลบ

    class Meta:
        model = Cow
        fields = ["name", "breed", "age", "weight", "price", "image", "pedigree_file"]
