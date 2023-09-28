from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Record
from dcrm.settings import BASE_DIR
import os
# Create your tests here.


class HomeTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="bob_test",password="qwerty")
   
    def setUp(self) -> None:
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def test_home(self):
        # self.client.logout()
        response = self.client.get(reverse("website:home"))
        self.assertContains(response, "Email")

# class CustomerRecordTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.user = User.objects.create_user(username="bob_test",password="qwerty")
    
#     @classmethod
#     def tearDownClass(cls) -> None:
#         cls.user.delete()
    
#     def setUp(self) -> None:
#         self.client.force_login(self.user)

#     def test_customer_record(self):
#         # self.client.logout()
#         id = User.objects.get(username="bob_test")
#         response = self.client.get(reverse("website:record", kwargs={"pk":id.pk}))
#         self.assertEqual(response.status_code, 200)

class AddRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="bob_test",password="qwerty")
   
    def setUp(self) -> None:
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def test_add_record(self):
        record = {
            "first_name": "",
            "last_name":"",
            "email":"",
            "phone": "",
            "address": "",
            "city": "",
            "state": "",
            "zipcode": "",
        }
        response = self.client.post(reverse("website:add_record"), data=record)
        self.assertEqual(response.status_code, 200)