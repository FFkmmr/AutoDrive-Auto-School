from django import forms
from django.utils import timezone
from datetime import date as date_cls, time as time_cls


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


class BookingForm(forms.Form):
    full_name = forms.CharField(
        label="Full name",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Имя, Фамилия, Отчество", "required": True}
        ),
    )
    phone = forms.CharField(
        label="Phone",
        max_length=32,
        widget=forms.TextInput(
            attrs={"placeholder": "+373   XX XXX XXX", "required": True}
        ),
    )
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"placeholder": "example@mail.com", "required": True}),
    )
    LESSON_CHOICES = [
        ("Теоретический экзамен категория В1/A1 - обычный", "Теоретический экзамен категория В1/A1 - обычный"),
        ("Практический экзамен категория В1/А1 - обычный", "Практический экзамен категория В1/А1 - обычный"),
        ("Теоретический экзамен категория В1/А1- срочный", "Теоретический экзамен категория В1/А1- срочный"),
        ("Практический экзамен категория В1/А1 - срочный", "Практический экзамен категория В1/А1 - срочный"),
    ]
    lesson_type = forms.ChoiceField(
        label="Lesson type",
        choices=LESSON_CHOICES,
        widget=forms.Select(attrs={"required": True}),
    )
    message = forms.CharField(
        label="Message",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Опишите что вас интересует и администрация автошколы ответит вам в ближайшее время...",
                "rows": 4,
            }
        ),
        max_length=2000,
    )
    date = forms.DateField(label="Date", widget=forms.DateInput(attrs={"type": "date", "required": True}))
    time = forms.TimeField(
        label="Time",
        required=False,
        widget=forms.TimeInput(attrs={"type": "time"}),
    )

    def clean(self):
        cleaned = super().clean()
        d = cleaned.get("date")
        t = cleaned.get("time")

        # Server-side guard: no past dates, and for today no past times
        if d:
            today = timezone.localdate()
            if d < today:
                self.add_error("date", "Нельзя выбрать прошедшую дату.")

            if t:
                now_local_time = timezone.localtime(timezone.now()).time()
                if d == today and t < now_local_time:
                    self.add_error("time", "Нельзя выбрать прошедшее время.")

        return cleaned
