from pprint import pprint

from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            path=reverse('users:register'),
            data={
                'username': 'abc',
                'first_name': 'abcname',
                'last_name': 'abclastname',
                'email': 'abc@gmail.com',
                'password': 'abcpassword'
            })

        user = CustomUser.objects.get(username='abc')

        self.assertEqual(user.first_name, 'abcname', 'name is not matched')
        self.assertEqual(user.last_name, 'abclastname')
        self.assertEqual(user.email, 'abc@gmail.com')
        self.assertNotEqual(user.password, 'abcpassword')
        self.assertTrue(user.check_password('abcpassword'))

    def test_required_fields(self):
        response = self.client.post(
            path=reverse('users:register'),
            data={
                'first_name': 'abcname',
                'last_name': 'abclastname',
            }
        )

        form = response.context['form']
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(form, 'username', 'This field is required.')
        self.assertFormError(form, 'password', 'This field is required.')

    def test_valid_email_address(self):
        response = self.client.post(
            path=reverse('users:register'),
            data={
                'username': 'abc',
                'first_name': 'abcname',
                'last_name': 'abclastname',
                'email': 'abcgmail.com',
                'password': 'abcpassword'
            })

        form = response.context['form']
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(form, 'email', 'Enter a valid email address.')

    def test_user_name_exists(self):
        self.client.post(
            path=reverse('users:register'),
            data={
                'username': 'abc',
                'first_name': 'abcname',
                'last_name': 'abclastname',
                'email': 'abc@gmail.com',
                'password': 'abcpassword'
            })

        user = CustomUser.objects.get(username='abc')


        response = self.client.post(
            path=reverse('users:register'),
            data={
                'username': 'abc',
                'first_name': 'abcname',
                'last_name': 'abclastname',
                'email': 'abc@gmail.com',
                'password': 'abcpassword'
            })

        user_count = CustomUser.objects.count()
        form = response.context['form']

        self.assertEqual(user_count, 1)
        self.assertFormError(form, 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.user_ = CustomUser.objects.create(
            username='abc', first_name='abcname', last_name='abclastname',
            email='abc@gmail.com'
        )
        self.user_.set_password('abcpass')
        self.user_.save()

    def text_successful_login(self):


        self.client.post(
            path=reverse('users:login'),
            data={
                'username': 'abc',
                'password': 'abcpass'
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):


        response = self.client.post(
            path=reverse('users:login'),
            data={
                'username': 'abcwrong',
                'password': 'abcpass'
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 401)

        response = self.client.post(
            path=reverse('users:login'),
            data={
                'username': 'abc',
                'password': 'abcpasswrong'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertEqual(response.status_code, 401)

    def test_logout(self):


        self.client.login(username='abc', password='abcpass')

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login')+'?next=/users/profile/')

    def test_login_function(self):
        user_ = CustomUser.objects.create(
            username='abc', first_name='abcname', last_name='abclastname',
            email='abc@gmail.com'
        )
        user_.set_password('abc')
        user_.save()

        self.client.login(username='abc', password='abc')

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_.username)
        self.assertContains(response, user_.first_name)
        self.assertContains(response, user_.last_name)
        self.assertContains(response, user_.email)

    def test_profile_update(self):
        user_ = CustomUser.objects.create(
            username='abc', first_name='abcname', last_name='abclastname',
            email='abc@gmail.com'
        )
        user_.set_password('abc')
        user_.save()

        self.client.login(username='abc', password='abc')

        self.client.post(
            reverse('users:profile_edit'),
            data={
                'username': 'def', 'first_name': 'defname', 'last_name': 'deflastname',
                "email":'def@gmail.com'
            }

        )

        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'def')
        self.assertContains(response, 'defname')
        self.assertContains(response, 'deflastname')
        self.assertContains(response, 'def@gmail.com')
        # print(response.__dict__)
        # self.assertEqual(response.path, reverse('users:profile'))
