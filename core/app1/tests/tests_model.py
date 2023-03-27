from django.db import IntegrityError
from django.test import TestCase
from django.core.exceptions import ValidationError
from app1.models import Student

class StudentModelTestCase(TestCase):
    def setUp(self):
        self.valid_student = Student.objects.create(name="Alice", div="A", mail="alice@example.com", mobile="1234567890")

    def test_valid_student(self):
        self.assertTrue(isinstance(self.valid_student, Student))
        self.assertEqual(str(self.valid_student), "Alice A alice@example.com 1234567890")

    def test_invalid_email(self):
        with self.assertRaises(ValidationError):
            invalid_student = Student.objects.create(name="Bob", div="B", mail="invalid-email", mobile="0987654321")
            invalid_student.full_clean()

    def test_unique_email(self):
        with self.assertRaises(ValidationError):
            duplicate_student = Student(name="Charlie", div="C", mail="alice@example.com", mobile="5555555555")
            duplicate_student.full_clean()
            duplicate_student.save()

class TestModelUniqueness(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name='something',
            div='A',
            mail='something@example.com',
            mobile='1234567890'
        )
    def test_unique_mail(self):
        # create a new instance of the model with unique mobile number
        instance = Student(name='John', div='123 Main St',mail='xyz@gmail.com', mobile='555-555-5555')
        instance.save()
        # check that the instance was successfully saved to the database
        self.assertEqual(Student.objects.filter(mail='xyz@gmail.com').count(), 1)

    def test_duplicate_mail(self):
        # create a new instance of the model with duplicate mobile number
        instance = Student(name='Jane', div='456 Park Ave',mail='something@example.com', mobile='555-555-5551')
        # check that an IntegrityError is raised when trying to save the duplicate mobile number
        # print(instance.save)
        self.assertRaises(IntegrityError, instance.save)








# class MyModelTest(TestCase):
#     def test_unique_field(self):
#         Student.objects.create(mail= "akshay@gmail.com")
#         try:
#             Student.objects.create(mail= "akshay@gmail.com")
#         except IntegrityError as e:
#             self.assertEqual(str(e), "UNIQUE constraint failed: app1_student.mail")
#         # else:
#         #     self.fail("Duplicate value allowed for unique field")

