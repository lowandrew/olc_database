from django.test import TestCase, Client
from django.urls import reverse
from olc_database.users.models import User


class ViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='TestUser')
        user.set_password('password')
        user.save()

    def test_query_builder_login_required(self):
        resp = self.client.get(reverse('data_wrapper:query_builder'))
        # Should be redirected!
        self.assertEqual(resp.status_code, 302)

    def test_query_builder_successful_load(self):
        self.client.login(username='TestUser', password='password')
        resp = self.client.get(reverse('data_wrapper:query_builder'))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'data_wrapper/query_builder.html')

    def test_table_builder_login_required(self):
        resp = self.client.get(reverse('data_wrapper:table_builder'))
        # Should be redirected!
        self.assertEqual(resp.status_code, 302)

    def test_table_builder_successful_load(self):
        self.client.login(username='TestUser', password='password')
        resp = self.client.get(reverse('data_wrapper:table_builder'))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'data_wrapper/table_builder.html')

