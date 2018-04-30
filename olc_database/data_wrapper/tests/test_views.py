from django.test import TestCase, Client
from django.urls import reverse
from olc_database.users.models import User
from data_wrapper.models import SavedQueries, SavedTables


class ViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='TestUser')
        user.set_password('password')
        user.save()
        SavedQueries.objects.create(user=user,
                                    search_terms=list(),
                                    search_attributes=list(),
                                    search_operations=list(),
                                    search_combine_operations=list(),
                                    query_name='TestQuery')
        SavedTables.objects.create(user=user,
                                   table_attributes=list(),
                                   table_name='TestTable')
        user = User.objects.create(username='BadUser')
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

    def test_saved_queries_login_required(self):
        resp = self.client.get(reverse('data_wrapper:saved_queries'))
        self.assertEqual(resp.status_code, 302)

    def test_saved_queries_successful_load(self):
        self.client.login(username='TestUser', password='password')
        resp = self.client.get(reverse('data_wrapper:saved_queries'))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'data_wrapper/saved_queries.html')

    def test_delete_query_confirm_successful(self):
        self.client.login(username='TestUser', password='password')
        query = SavedQueries.objects.get(user=User.objects.get(username='TestUser'))
        resp = self.client.get(reverse('data_wrapper:delete_query_confirm', kwargs={'query_id': query.id}))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'data_wrapper/delete_query_confirm.html')

    def test_delete_query_wrong_user(self):
        self.client.login(username='BadUser', password='password')
        query = SavedQueries.objects.get(user=User.objects.get(username='TestUser'))
        resp = self.client.get(reverse('data_wrapper:delete_query_confirm', kwargs={'query_id': query.id}))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, '403.html')

    def test_delete_table_confirm_successful(self):
        self.client.login(username='TestUser', password='password')
        table = SavedTables.objects.get(user=User.objects.get(username='TestUser'))
        resp = self.client.get(reverse('data_wrapper:delete_table_confirm', kwargs={'table_id': table.id}))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'data_wrapper/delete_table_confirm.html')

    def test_delete_table_wrong_user(self):
        self.client.login(username='BadUser', password='password')
        table = SavedTables.objects.get(user=User.objects.get(username='TestUser'))
        resp = self.client.get(reverse('data_wrapper:delete_table_confirm', kwargs={'table_id': table.id}))
        # Should be successful! Also test that correct template used.
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, '403.html')
