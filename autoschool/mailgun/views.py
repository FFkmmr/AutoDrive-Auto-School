from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

import requests

from .forms import FeedbackForm, BookingForm


def _send_mailgun(subject: str, text: str, reply_to: str | None = None) -> tuple[bool, str]:
	"""
	Send a plain-text email via Mailgun HTTP API.

	Returns (ok, detail).
	"""
	api_key = getattr(settings, "MAILGUN_API_KEY", None)
	domain = getattr(settings, "MAILGUN_DOMAIN", None)
	sender = getattr(settings, "MAILGUN_FROM", None)
	recipient = getattr(settings, "MAILGUN_TO", None)
	base_url = getattr(settings, "MAILGUN_API_BASE_URL", "https://api.mailgun.net/v3")

	if not all([api_key, domain, sender, recipient]):
		return (
			False,
			"Mailgun is not configured. Please set MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_FROM, MAILGUN_TO in settings or environment.",
		)

	url = f"{base_url}/{domain}/messages"
	# Support multiple recipients: comma- or semicolon-separated string -> list
	recipients: list[str] = []
	if isinstance(recipient, (list, tuple)):
		recipients = [str(r).strip() for r in recipient if str(r).strip()]
	elif isinstance(recipient, str):
		recipients = [r.strip() for r in recipient.replace(";", ",").split(",") if r.strip()]

	data: dict[str, str | list[str]] = {
		"from": sender,
		"to": recipients or recipient,
		"subject": subject,
		"text": text,
	}
	if reply_to:
		data["h:Reply-To"] = reply_to

	try:
		resp = requests.post(url, auth=("api", api_key), data=data, timeout=10)
		if 200 <= resp.status_code < 300:
			return True, "Message sent successfully."
		return False, f"Mailgun error {resp.status_code}: {resp.text}"
	except requests.RequestException as exc:
		return False, f"Request failed: {exc}"


def _send_via_mailgun(email: str, message: str) -> tuple[bool, str]:
	"""Back-compat helper for feedback route."""
	subject = "AutoDrive: New feedback message"
	text = f"From: {email}\n\n{message}"
	return _send_mailgun(subject=subject, text=text, reply_to=email)


@require_POST
def send_feedback(request):
	"""Handle feedback form submission and send via Mailgun."""
	form = FeedbackForm(request.POST)
	if not form.is_valid():
		messages.error(request, "Please provide a valid email and message.")
		# Redirect back to the referring page or home if not available
		return redirect(request.META.get("HTTP_REFERER", reverse("home")))

	email = form.cleaned_data["email"]
	message = form.cleaned_data["message"]

	ok, detail = _send_via_mailgun(email=email, message=message)
	if ok:
		messages.success(request, "Ваше сообщение отправлено!")
	else:
		messages.error(request, f"Не удалось отправить сообщение: {detail}")

	return redirect(request.META.get("HTTP_REFERER", reverse("home")))


@require_POST
def send_booking(request):
	"""Handle booking form submission and send via Mailgun."""
	form = BookingForm(request.POST)
	if not form.is_valid():
		messages.error(request, "Проверьте корректность данных формы записи.")
		return redirect(request.META.get("HTTP_REFERER", reverse("booking")))

	cd = form.cleaned_data
	full_name = cd["full_name"]
	phone = cd["phone"]
	email = cd["email"]
	lesson_type = cd["lesson_type"]
	user_message = cd.get("message") or ""
	date = cd["date"].strftime("%Y-%m-%d")
	time = cd.get("time")
	time_str = time.strftime("%H:%M") if time else "—"

	subject = "AutoDrive: Новая запись"
	text_lines = [
		f"Имя: {full_name}",
		f"Телефон: {phone}",
		f"Email: {email}",
		f"Тип урока: {lesson_type}",
		f"Дата: {date}",
		f"Время: {time_str}",
		"",
		"Сообщение:",
		user_message,
	]
	text = "\n".join(text_lines)

	ok, detail = _send_mailgun(subject=subject, text=text, reply_to=email)
	if ok:
		messages.success(request, "Заявка отправлена. Мы свяжемся с вами!")
	else:
		messages.error(request, f"Не удалось отправить заявку: {detail}")

	return redirect(request.META.get("HTTP_REFERER", reverse("booking")))
