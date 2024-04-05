from django import forms
from .models import Language, Entry, Translation, Vote


class AddEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["lang", "content"]

        widgets = {
            "lang": forms.Select(attrs={"class": "form-select mb-2",
                                        "id": "lang"}),
            "content": forms.Textarea(attrs={"class": "form-control px-4 py-3 m-0",
                                             "id": "text-input",}),
        }


class AddTranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ["lang", "content"]

        widgets = {
            "lang": forms.Select(attrs={"class": "form-select mb-2",
                                        "id": "lang"}),
            "content": forms.Textarea(attrs={"class": "form-control mb-2",
                                             "id": "content",}),
        }