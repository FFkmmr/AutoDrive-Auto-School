from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, Mock


class FeedbackViewTests(TestCase):
	def test_invalid_form_shows_error(self):
		resp = self.client.post(reverse("mailgun:send_feedback"), data={
			"email": "not-an-email",
			"message": "Hello",
		})
		self.assertEqual(resp.status_code, 302)  # redirect back

	@patch("mailgun.views.requests.post")
	@patch("mailgun.views.settings")
	def test_valid_submission_sends_mailgun(self, settings_mock, post_mock):
		# Configure settings for the view
		settings_mock.MAILGUN_API_KEY = "key-test"
		settings_mock.MAILGUN_DOMAIN = "example.com"
		settings_mock.MAILGUN_FROM = "AutoDrive <noreply@example.com>"
		settings_mock.MAILGUN_TO = "admin@example.com"
		settings_mock.MAILGUN_API_BASE_URL = "https://api.mailgun.net/v3"

		# Mock Mailgun success response
		response = Mock()
		response.status_code = 200
		response.text = "Queued. Thank you."
		post_mock.return_value = response

		resp = self.client.post(reverse("mailgun:send_feedback"), data={
			"email": "user@example.com",
			"message": "Test message",
		})

		self.assertEqual(resp.status_code, 302)
		post_mock.assert_called_once()
