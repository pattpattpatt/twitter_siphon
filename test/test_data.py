import unittest
from data.models import mentions
from data.models import congress


class TestMentions(unittest.TestCase):
    def setUp(self):
        pass

    def test_master_users_init(self):
        list = mentions._users_list_init(mentions._from_static_list, user_list=congress.congress_users())
        self.assertTrue(list)
