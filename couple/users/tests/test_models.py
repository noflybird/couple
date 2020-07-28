import pytest

from couple.users.models import User

pytestmark = pytest.mark.django_db

from test_plus.test import TestCase

#
# def test_user_get_absolute_url(user: User):
#     assert user.get_absolute_url() == f"/users/{user.username}/"


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(self.user.__str__(), 'testuser')

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/users/testuser/')

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == 'testuser'
        self.user.nickname = u"昵称"
        assert self.user.get_profile_name() == u"昵称"
