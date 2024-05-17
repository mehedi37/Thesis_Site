from django import forms
from .models import ThesisApply


class ThesisApplyForm(forms.ModelForm):
    class Meta:
        model = ThesisApply
        fields = ['message', 'cv']
