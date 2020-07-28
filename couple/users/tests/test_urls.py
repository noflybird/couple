import pytest
from django.urls import resolve, reverse

from couple.users.models import User
from test_plus.test import TestCase

pytestmark = pytest.mark.django_db


class TestUserURLs(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail', kwargs={'username': "testuser"}), '/users/testuser/')

    def test_detail_resolve(self):
        self.assertEqual(resolve('/users/testuser/').view_name, 'users:detail')

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'), '/users/update/')

    def test_update_resolve(self):
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')
