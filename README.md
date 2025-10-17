User authorization via JWT
-----------------------------

cd backend/
Starting development server at http://127.0.0.1:8001/




Register User
enter in terminal

Endpoint: POST /api/register/
-----------------------------
curl -X POST "http://127.0.0.1:8001/api/register/" \ 
-H "Content-Type: application/json" \                     
-d '{"username": "testuser3", "password": "jena12345678"}'


terminal output
-----------------------------

{"id":3,"username":"testuser3","email":""}%     




Login User
Endpoint: POST /api/login/
-----------------------------
curl -X POST "http://127.0.0.1:8001/api/login/" \
-H "Content-Type: application/json" \
-d '{"username": "testuser2", "password": "jena12345678"}'

terminal output
-----------------------------

{
  "refresh": "<REFRESH_TOKEN>",
  "access": "<ACCESS_TOKEN>"
}



Refresh User
Endpoint: POST /api/token/refresh/
-----------------------------
curl -X POST "http://127.0.0.1:8001/api/token/refresh/" \
-H "Content-Type: application/json" \
-d '{"refresh": "<YOUR_REFRESH_TOKEN>"}'


terminal output  token change
-----------------------------

{

  "access": "<ACCESS_TOKEN>"
}

After logging in, go to Stripe
-----------------------------

curl -X POST "http://127.0.0.1:8001/api/create-stripe-customer/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <ACCESS_TOKEN>"

terminal output  token change
-----------------------------
{
  "message": "Stripe session created successfully!",
  "session_id": "cs_test_a1Op4xzuVPlOiIRQPadUpmuv2bw1Bhf6oyD0jIfdMAGHplovWr355ubPCe",
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_test_a1Op4xzuVPlOiIRQPadUpmuv2bw1Bhf6oyD0jIfdMAGHplovWr355ubPCe"
}

--------------shell---------------------------------
cd backend
python manage.py shell

from api.models import StripeCustomer
d = StripeCustomer.objects.get(user__username="testuser3")
print(d.user.username)       # testuser3
print(d.session_id)          #  session_id 
print(d.stripe_customer_id)  # ID Stripe

--------------shell---------------------------------

-----------------------------test-----------------------------

backend/api/tests

--------------shell---------------------------------
python manage.py test

Found 2 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 2.015s



-----------------------------test-----------------------------


