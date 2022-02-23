from django.test import TestCase
from django.contrib.auth import get_user_model
from flask import request
from rest_framework.test import APIRequestFactory, force_authenticate
from .views import PostList, PostRetriveDestroy
from rest_framework.serializers import ErrorDetail
# Create your tests here.

User = get_user_model()

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User(username='test', email='test@test.com')
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.set_password('some_123_pass')
        self.user.save()
        self.factory = APIRequestFactory()
        self.create_view = PostList.as_view()
        self.post_retrive_view = PostRetriveDestroy.as_view()
    
    def test_user_exists(self):
        total_users = User.objects.all().count()
        self.assertEqual(total_users, 1)
    
    def test_posts_creation(self):
        data = {
            "title": "foo",
            "url": "https://www.django-rest-framework.org/api-guide/testing/",
        }
        request = self.factory.get('api/posts')
        response = self.create_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

        request = self.factory.post('api/posts/', data=data)
        force_authenticate(request=request, user=self.user)
        response = self.create_view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user.get_username() == response.data.get('poster'))

        request = self.factory.get('api/posts')
        response = self.create_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


    def test_get_post_by_id(self):
        data = {
            "title": "foo",
            "url": "https://www.django-rest-framework.org/api-guide/testing/",
        }

        request = self.factory.post('api/posts/', data=data)
        force_authenticate(request=request, user=self.user)
        response = self.create_view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user.get_username() == response.data.get('poster'))

        post_id = response.data.get('id')
        new_post = response.data

        request = self.factory.get(f'api/posts/{post_id}')
        response = self.post_retrive_view(request, pk=post_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, new_post)

    def test_delete_post_by_id(self):
        data = {
            "title": "foo",
            "url": "https://www.django-rest-framework.org/api-guide/testing/",
        }

        request = self.factory.post('api/posts/', data=data)
        force_authenticate(request=request, user=self.user)
        response = self.create_view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user.get_username() == response.data.get('poster'))

        post_id = response.data.get('id')

        request = self.factory.delete(f'api/posts/{post_id}')
        force_authenticate(request=request, user=self.user)
        response = self.post_retrive_view(request, pk=post_id)

        self.assertEqual(response.status_code, 204)

        request = self.factory.get(f'api/posts/{post_id}')
        response = self.post_retrive_view(request, pk=post_id)
        self.assertEqual(response.status_code, 404)


    def test_delete_post_from_new_user(self):
        data = {
            "title": "foo",
            "url": "https://www.django-rest-framework.org/api-guide/testing/",
        }

        request = self.factory.post('api/posts/', data=data)
        force_authenticate(request=request, user=self.user)
        response = self.create_view(request)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.user.get_username() == response.data.get('poster'))

        post_id = response.data.get('id')
        new_post = response.data

        new_user = User(username='foo', email='foo@test.com')
        new_user.set_password('some_123_pass')
        new_user.save()

        request = self.factory.delete(f'api/posts/{post_id}')
        force_authenticate(request=request, user=new_user)
        response = self.post_retrive_view(request, pk=post_id)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, [ErrorDetail(string="You cannot delete other person's post !!", code='invalid')])

        request = self.factory.get(f'api/posts/{post_id}')
        response = self.post_retrive_view(request, pk=post_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, new_post)
