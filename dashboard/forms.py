from django import forms
from .models import ExpenseInfo

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = ExpenseInfo
        fields = ["name", "amount", "category"]