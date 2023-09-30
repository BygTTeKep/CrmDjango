from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from .models import Record
from .forms import AddRecordForm, SignUpForm
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

class CustomerRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="bob_test",password="qwerty")
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
    
    def setUp(self) -> None:
        self.client.force_login(self.user)
        record = {
            "first_name": "123",
            "last_name":"123",
            "email":"123",
            "phone": "123",
            "address": "123",
            "city": "123",
            "state": "123",
            "zipcode": "123S",
        }
        self.recordData = Record.objects.create(first_name=record["first_name"],
                                                last_name=record["last_name"],
                                                email=record["email"],
                                                phone=record["phone"],
                                                address=record["address"],
                                                city=record["city"],
                                                state=record["state"],
                                                zipcode=record["zipcode"]
                                                )
    def test_customer_record(self):
        id = User.objects.get(username="bob_test")
        response = self.client.get(reverse("website:record", kwargs={"pk":id.pk}))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response = self.client.get(reverse("website:record", kwargs={"pk":id.pk}))
        self.assertEqual(response.status_code, 302)

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
        record = [
            {
                "name": "valid",
                "status_code": 302,
                "value":{
                    "first_name": "123",
                    "last_name":"123",
                    "email":"123",
                    "phone": "123",
                    "address": "123",
                    "city": "123",
                    "state": "123",
                    "zipcode": "123S",
                },
            },
            {
                "name": "not valid[first_name]",
                "status_code": 400,
                "value":{
                    "last_name":"123",
                    "email":"123",
                    "phone": "123",
                    "address": "123",
                    "city": "123",
                    "state": "123",
                    "zipcode": "123S",
                },
            },
        ]
        for val in record:
            response = self.client.post(reverse("website:add_record"), data=val["value"])
            # self.assertRedirects(response, reverse('website:home'))
            self.assertEqual(response.status_code, val["status_code"])

class AddRecordFormTestCase(TestCase):
    '''
        Тестирование формы
        https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/Testing
    '''
    def test_add_record_form(self):
        record = [
            {
                "name": "valid",
                "valid": True,
                "value":{
                    "first_name": "123",
                    "last_name":"123",
                    "email":"123",
                    "phone": "123",
                    "address": "123",
                    "city": "123",
                    "state": "123",
                    "zipcode": "123S",
                },
            },
            {
                "name": "not valid[first_name]",
                "valid": False,
                "value":{
                    "last_name":"123",
                    "email":"123",
                    "phone": "123",
                    "address": "123",
                    "city": "123",
                    "state": "123",
                    "zipcode": "123S",
                },
            }
        ]
        for val in record:
            form = AddRecordForm(data=val["value"])
            self.assertEqual(form.is_valid(), val["valid"])

class SignUpFormTestCase(TestCase):
    def test_signup_form(self):
        tc = [
            {
                "name": "valid",
                "valid": True,
                "value":{
                    "username": "asdafea",
                    "first_name": "asdafea",
                    "last_name": "asdafea",
                    "email": "123@mail.ru",
                    "password1": "asjfekhfiuwahriufasf123",
                    "password2": "asjfekhfiuwahriufasf123",
                }
            },
            {
                "name": "not valid[email]",
                "valid": False,
                "value":{
                    "username": "asdafea",
                    "first_name": "asdafea",
                    "last_name": "asdafea",
                    "email": "asfasfw",
                    "password1": "asjfekhfiuwahriufasf123",
                    "password2": "asjfekhfiuwahriufasf123",
                }
            },
            {
                "name": "not valid[password]",
                "valid": False,
                "value":{
                    "username": "asdafea",
                    "first_name": "asdafea",
                    "last_name": "asdafea",
                    "email": "123@mail.ru",
                    "password1": "asjfekhfiuwahriufasf123",
                    "password2": "123",
                }
            },
                        {
                "name": "not valid[username]",
                "valid": False,
                "value":{
                    "first_name": "asdafea",
                    "last_name": "asdafea",
                    "email": "123@mail.ru",
                    "password1": "asjfekhfiuwahriufasf123",
                    "password2": "asjfekhfiuwahriufasf123",
                }
            },
                        {
                "name": "not valid[first_name]",
                "valid": False,
                "value":{
                    "username": "asdafea",
                    "last_name": "asdafea",
                    "email": "123@mail.ru",
                    "password1": "asjfekhfiuwahriufasf123",
                    "password2": "asjfekhfiuwahriufasf123",
                }
            },
                        {
                "name": "not valid[last_name]",
                "valid": False,
                "value":{
                    "username": "asdafea",
                    "first_name": "asdafea",
                    "email": "123@mail.ru",
                    "password1": "asjfekhfiuwahriufasf123",
                    "password2": "123",
                }
            }
        ]
        for val in tc:
            print(val["name"])
            form = SignUpForm(data=val["value"])
            self.assertEqual(form.is_valid(), val["valid"])

class UpdateRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="bob_test",password="qwerty")
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
    
    def setUp(self) -> None:
        self.client.force_login(self.user)
        record = {
            "first_name": "123",
            "last_name":"123",
            "email":"123",
            "phone": "123",
            "address": "123",
            "city": "123",
            "state": "123",
            "zipcode": "123S",
        }
        self.recordData = Record.objects.create(first_name=record["first_name"],
                                                last_name=record["last_name"],
                                                email=record["email"],
                                                phone=record["phone"],
                                                address=record["address"],
                                                city=record["city"],
                                                state=record["state"],
                                                zipcode=record["zipcode"]
                                            )
    def tes_update_record(self):
        testCaseRecord = [
            {
                "name": "valid",
                "status_code": 201,
                "value":{
                    "username": "asdafea",
                }
            },
            {
                "name": "not valid",
                "status_code": 400,
                "value":{
                    "username": "123456789012345678901234567890123456789012345678901234567890",
                }
            }
        ]
        id = Record.objects.get(first_name="123")
        for tc in testCaseRecord:
            response = self.client.post(reverse("website:update_record", kwargs={"pk":id.pk}), data=tc["value"])
            self.assertEqual(response.status_code, tc["status_code"])


class DeleteRecordTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="bob_test",password="qwerty")
    
    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
    
    def setUp(self) -> None:
        self.client.force_login(self.user)
        record = {
            "first_name": "123",
            "last_name":"123",
            "email":"123",
            "phone": "123",
            "address": "123",
            "city": "123",
            "state": "123",
            "zipcode": "123S",
        }
        self.recordData = Record.objects.create(first_name=record["first_name"],
                                                last_name=record["last_name"],
                                                email=record["email"],
                                                phone=record["phone"],
                                                address=record["address"],
                                                city=record["city"],
                                                state=record["state"],
                                                zipcode=record["zipcode"]
                                            )
    def test_delete_record(self):
        id = Record.objects.get(first_name="123")
        response = self.client.post(reverse("website:delete_record", kwargs={"pk":id.pk}))
        self.assertEqual(response.status_code, 302)