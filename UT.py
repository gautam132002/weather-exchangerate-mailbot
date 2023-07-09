import unittest
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import re
from unittest.mock import patch, MagicMock
from program import is_valid_email
import program

OPENWEATHERMAP_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHERMAP_API_KEY = "4b0a9096534179f10a0ac5255a8d218b"
GMAIL_ADDRESS = "demoscript2002@gmail.com"
GMAIL_PASSWORD = "wzogippwniqeglid"

class TestIsValidEmail(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(is_valid_email("example@example.com"))
        self.assertTrue(is_valid_email("example123@example.com"))
        self.assertTrue(is_valid_email("example+123@example.com"))

    def test_invalid_email(self):
        self.assertFalse(is_valid_email("example"))
        self.assertFalse(is_valid_email("example@"))
        self.assertFalse(is_valid_email("example@.com"))
        self.assertFalse(is_valid_email("example.com"))

    def test_get_weather_data_success(self):
        expected_output = "Current weather in your city: clear sky. Temperature: 9.56°C"
        requests = MagicMock()
        requests.get.return_value.json.return_value = {
            "weather": [{"description": "clear sky"}],
            "main": {"temp": 282.71}
        }
        program.requests = requests
        output = program.get_weather_data()
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
