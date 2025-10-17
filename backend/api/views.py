from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import stripe
from django.conf import settings
from .models import StripeCustomer
from rest_framework.decorators import api_view, permission_classes

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Проверяем, есть ли уже StripeCustomer для этого пользователя
        stripe_customer, created = StripeCustomer.objects.get_or_create(user=user)

        # Если клиент ещё не зарегистрирован в Stripe — создаём
        if not stripe_customer.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.username,
            )
            stripe_customer.stripe_customer_id = customer.id
            stripe_customer.save()

        # Создаём checkout session
        session = stripe.checkout.Session.create(
            customer=stripe_customer.stripe_customer_id,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Test Payment'},
                    'unit_amount': 1000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )

        # Обновляем session_id в БД
        stripe_customer.session_id = session.id
        stripe_customer.save()

        return Response({
            "message": "Stripe session created successfully!",
            "session_id": session.id,
            "checkout_url": session.url
        })


# class CreateStripeCustomerView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user

#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {'name': 'Test Payment'},
#                     'unit_amount': 1000,
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url='https://example.com/success',
#             cancel_url='https://example.com/cancel',
#         )

#         StripeCustomer.objects.create(user=user, session_id=session.id)

#         return Response({
#             "message": "Stripe session created successfully!",
#             "session_id": session.id,
#             "checkout_url": session.url
#         })

# class TestAuthView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({"message": f"Привет, {request.user.username}!"})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class TokenRefreshViewCustom(TokenRefreshView):
    permission_classes = [AllowAny]