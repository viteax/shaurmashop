from django.test.client import Client
from django.urls import reverse

client = Client()

response = client.get('')
print(response.status_code)
