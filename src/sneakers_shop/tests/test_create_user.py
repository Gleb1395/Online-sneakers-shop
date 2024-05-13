from django.contrib.auth import get_user_model
from django.test import TestCase
#Some changes


class TestCreateUser(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name="test",
            last_name="test2",
            email="test@example.com",
            password="123456789",
        )
