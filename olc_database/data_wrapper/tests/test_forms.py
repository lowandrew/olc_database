from django.test import TestCase
from data_wrapper.forms import SearchForm, CustomTableForm


class FormTests(TestCase):
    def test_search_form_valid(self):
        form_data = {'search_attribute': 'genus',
                     'search_item': 'asdf',
                     'operation': 'CONTAINS',
                     'combine_choice': 'AND'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_missing_attribute(self):
        form_data = {'search_item': 'asdf',
                     'operation': 'CONTAINS',
                     'combine_choice': 'AND'}
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_table_form_valid(self):
        form_data = {'table_attribute': 'genus'}
        form = CustomTableForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_table_form_invalid(self):
        form_data = {}
        form = CustomTableForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_table_form_invalid_blank(self):
        form_data = {'table_attribute': ''}
        form = CustomTableForm(data=form_data)
        self.assertFalse(form.is_valid())
