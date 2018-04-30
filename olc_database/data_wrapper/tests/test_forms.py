from django.test import TestCase
from data_wrapper.forms import SearchForm, CustomTableForm, SeqTrackingCreateForm


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

    def test_seqtracking_create_valid(self):
        form_data = {'seqid': '2012-SEQ-0021',
                     'lsts_id': 'asdf',
                     'location': 'BMH',
                     'oln_id': 'a_new_oln_id',
                     'project': 'a_new_project',
                     'priority': 'RESEARCH',
                     'curator_flag': 'PASS',
                     'comment': 'a comment'}
        form = SeqTrackingCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_seqtracking_create_valid_nocomment(self):
        form_data = {'seqid': '2012-SEQ-0021',
                     'lsts_id': 'asdf',
                     'location': 'BMH',
                     'oln_id': 'a_new_oln_id',
                     'project': 'a_new_project',
                     'priority': 'RESEARCH',
                     'curator_flag': 'PASS'}
        form = SeqTrackingCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_seqtracking_invalid_seqid(self):
        form_data = {'seqid': '20122-SEQ-0021',
                     'lsts_id': 'asdf',
                     'location': 'BMH',
                     'oln_id': 'a_new_oln_id',
                     'project': 'a_new_project',
                     'priority': 'RESEARCH',
                     'curator_flag': 'PASS',
                     'comment': 'a comment'}
        form = SeqTrackingCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
