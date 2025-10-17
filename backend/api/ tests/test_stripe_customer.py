from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from api.models import StripeCustomer
import stripe
from unittest import mock



class StripeCustomerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser3", password="testpassword")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.url = "/api/create-stripe-customer/"

    @mock.patch("stripe.checkout.Session.create")
    @mock.patch("stripe.Customer.create")
    def test_create_stripe_session_new_user(self, mock_customer_create, mock_session_create):
        mock_customer_create.return_value.id = "cus_test123"
        mock_session_create.return_value.id = "cs_test123"
        mock_session_create.return_value.url = "https://checkout.stripe.com/test"

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["session_id"], "cs_test123")

        stripe_customer = StripeCustomer.objects.get(user=self.user)
        self.assertEqual(stripe_customer.stripe_customer_id, "cus_test123")
        self.assertEqual(stripe_customer.session_id, "cs_test123")

    def test_access_without_token(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)