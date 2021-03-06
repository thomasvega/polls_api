from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


from polls import views

class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object
        """
        url = reverse('user_create')
        data = {'username': 'test', 'email': 'test@test.com', 'password': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email,'test@test.com')

class TestPoll(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = views.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
    
    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_list(self):
        request = self.factory.get(self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200, 'Excepted Response Code 200, received {0} instead.'.format(response.status_code))
    
    def test_list2(self):
        self.client.login(username="test", password="test")
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200, 'Excepted Response Code 200, received {0} instead.'.format(response.status_code))
    
    def test_create(self):
        self.client.login(username="test", password="test")
        params = {
            "question": "How are you?",
            "created_by": 1
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
                        'Expected Response Code 201, received {0} instead.'.format(response.status_code))
