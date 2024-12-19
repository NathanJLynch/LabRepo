from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from TA_Scheduler.models import User

class TestAccountDeletion(TestCase):
    def setUp(self):
        self.full_name = 'John Doe'
        self.password = 'Hello!123'
        self.email = 'hi@uwm.edu'
        self.role = 'admin'
        User.objects.create(full_name=self.full_name, email=self.email, password=self.password,
                            role_id=self.role)

    def test_delete_account(self):
        User.objects.get(full_name = self.full_name).delete()
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name= self.full_name)
        # side effect : email sent

    def test_delete_nonexistent_user(self):
        User.objects.get(full_name=self.full_name).delete()
        self.assertEqual(User.objects.count(), 0)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(full_name=self.full_name).delete()


