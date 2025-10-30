from django import forms


class FeedbackForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Email...",
            "required": True,
        }),
        max_length=254,
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            "placeholder": "Опишите что вас интересует...",
            "rows": 4,
            "required": True,
        }),
        max_length=2000,
    )
