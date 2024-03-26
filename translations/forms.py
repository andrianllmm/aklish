from django import forms
from .models import Language, Entry, Translation, Vote


class AddEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["lang", "content"]

        widgets = {
            "lang": forms.Select(attrs={"class": "form-select mb-2",
                                        "id": "lang"}),
            "content": forms.Textarea(attrs={"class": "form-control mb-2",
                                             "id": "content",
                                             "placeholder": "Type what you want to be translated here..."}),
        }

    translation_lang = forms.ModelChoiceField(
        queryset=Language.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select mb-2",
                                   "id": "translation_lang"})
    )
    translation_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control mb-2",
                                     "id": "translation_content",
                                     "placeholder": "Type your translation here..."}),
    )


class AddTranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ["lang", "content"]

        widgets = {
            "lang": forms.Select(attrs={"class": "form-select mb-2",
                                        "id": "lang"}),
            "content": forms.Textarea(attrs={"class": "form-control mb-2",
                                             "id": "content",
                                             "placeholder": "Type your translation here..."}),
        }