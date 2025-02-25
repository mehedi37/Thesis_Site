from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from supervisor.models import Supervisor

class LoginTest(TestCase):
  def setUp(self):
    self.client = Client()
    self.register_admin_url = reverse('register_admin')
    self.login_url = reverse('login')
    self.userDetails = {
        'username': 'testadmin',
        'password1': 'testpassword',
        'password2': 'testpassword',
        'email': 'test@g.com',
        'account_type': 'supervisor'
      }

  def test_01_register_view_get(self):
    try:
      response = self.client.get(self.register_admin_url)
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'register_admin.html')
      print("✅ REGISTER: GET request test passed.")
    except Exception as e:
      print(f"❌ REGISTER: GET request test failed: {e}")

  def test_02_register_view_post(self):
    try:
      response = self.client.post(self.register_admin_url, self.userDetails)

      self.assertEqual(response.status_code, 302)
      self.assertRedirects(response, reverse('login'))
      print("✅ REGISTER: POST request test passed.")
    except Exception as e:
      print(f"❌ REGISTER: POST request test failed: {e}")

  def test_03_login_view_get(self):
    try:
      response = self.client.get(self.login_url)
      self.assertEqual(response.status_code, 200)
      self.assertTemplateUsed(response, 'login.html')
      print("✅ LOGIN: GET request test passed.")
    except Exception as e:
      print(f"❌ LOGIN: GET request test failed: {e}")

  def test_04_login_view_post_valid(self):
    try:
      user = User.objects.create_user(
        username=self.userDetails['username'],
        password=self.userDetails['password1']
      )

      Supervisor.objects.create(user=user)

      response = self.client.post(self.login_url, {
          'username': self.userDetails['username'],
          'password': self.userDetails['password1'],
          'account_type': self.userDetails['account_type']
      }, follow=True)

      self.assertRedirects(
          response,
          reverse('project_list'),
          status_code=302,
          target_status_code=200
      )
      print("✅ LOGIN: POST request test with valid credentials passed.")
    except Exception as e:
      print(f"❌ LOGIN: POST request test with valid credentials failed: {e}")