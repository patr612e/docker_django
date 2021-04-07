from django import forms
from .models import Costumer, User

class CostumerForm(forms.ModelForm):
    class Meta:
        model = Costumer
        exclude = ()

class AddCostumer(forms.Form):
    phone = forms.CharField()
    rank = forms.CharField()
    is_employee = forms.BooleanField(required=False)


