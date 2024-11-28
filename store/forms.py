from .models import Rateing
from django import forms
class RateForm(forms.ModelForm):
    
    class Meta:
        model=Rateing
        fields=["star","review"]
        widgets={
            "review":forms.TextInput(attrs={"class":"form-control"}),
            "star":forms.ChoiceField()
        }