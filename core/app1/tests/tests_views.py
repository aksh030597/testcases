from django.forms import ValidationError
from django.test import TestCase
from app1.models import Student
from rest_framework.test import APIClient
from rest_framework import status





class StudentTest(TestCase):
    def test_valid_email(self):
        student = Student(name='John Doe', div='A', mail='johndoe@gmail.com', mobile='1234567890')
        self.assertEqual(student.clean_fields(), None)

    def test_invalid_email(self):
        student = Student(name='John Doe', div='A', mail='invalid', mobile='1234567890')
        self.assertRaises(ValidationError, student.clean_fields)



class StudentTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student1 = Student.objects.create(
            id='0ee814e2-5a93-43f8-965d-31b2a87a1d69', name='Akshay', div='A', mail='akshay@gmail.com', mobile= '1234567890')
        self.student2 = Student.objects.create(
            id='e564e7ca-ac56-4dcb-ab7a-981614b04f15', name='shubham', div='B', mail='shubham@gmail.com', mobile= '987654321')
      

    def test_get_all_students(self):
        # get API response
        response = self.client.get('/student/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [
            {'id':'0ee814e2-5a93-43f8-965d-31b2a87a1d69', 'name':'Akshay', 'div':'A', 'mail':'akshay@gmail.com', 'mobile': '1234567890'},
            {'id':'e564e7ca-ac56-4dcb-ab7a-981614b04f15', 'name':'shubham', 'div':'B', 'mail':'shubham@gmail.com', 'mobile': '987654321'}
        ])

    
    def test_invalid_get_all_students(self):
        # get API response
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

 
    def test_post_student(self):
        # create a new student
        response = self.client.post('/student/', {'name': 'John', 'div': 'C', 'mail': 'john@gmail.com', 'mobile': '1231231234'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 3)
        self.assertEqual(response.json(), {'data': {'name': 'John', 'div': 'C', 'mail': 'john@gmail.com', 'mobile': '1231231234'}})
  
    def test_invalid_email_address(self):
        data = {'name': 'John', 'div': 'A', 'mail': 'invalid_email', 'mobile': '1234567890'}
        response = self.client.post('/student/', data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json(),{"status": "error", "error_code": 103, "message": "error: ['Enter a valid email address.'] "})
   
    def test_invalid_post_student(self):
        # create a new student without pass mobile key
        response = self.client.post('/student/', {'name': 'John', 'div': 'C', 'mail': 'john@gmail.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class StudentPutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student_data = {'name': 'Jonny', 'div': 'C', 'mail': 'jonny@gmail.com', 'mobile': '3692581470'} 
        self.response = self.client.post('/student/', self.student_data)
        self.student = Student.objects.get()


    def test_put_student(self):
        # update an existing student
        new_data = {'id':self.student.id, 'name': 'Akshay', 'div': 'A', 'mail': 'akshaygupta@gmail.com', 'mobile': '9876543210'}
        response = self.client.put('/student/', data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # expected_response = {
        #     'data': {
        #         'id': uuid.UUID('63383bd2-0083-4344-b913-2e28797d6cb5'),
        #         'name': 'Akshay',
        #         'div': 'A',
        #         'mobile': '9876543210',
        #         'mail': 'akshaygupta@gmail.com'
        #     }
        # }

        # self.assertEqual(response.json(), expected_response)
        # self.assertEqual(response.json(), {'data': {'id': self.student.id, 'name': 'Akshay', 'div': 'A', 'mobile': '9876543210', 'mail': 'akshaygupta@gmail.com'}})

    def test_put_invalid_email_address(self):
        new_data = {'id':self.student.id, 'name': 'John', 'div': 'A', 'mail': 'invalid_email', 'mobile': '1234567890'}
        response = self.client.put('/student/', new_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json(),{"status": "error", "error_code": 103, "message": "error: ['Enter a valid email address.'] "})
   
    def test_put_invalid_student(self):
        # create a new student without pass mobile key
        new_data = {'id':self.student.id, 'name': 'Akshay', 'div': 'A', 'mail': 'akshaygupta@gmail.com'}
        response = self.client.put('/student/',new_data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_patch_student(self):
        # update an existing student
        new_data = {'id':self.student.id, 'name': 'Akshay', 'mobile': '11111111'}
        response = self.client.patch('/student/', data=new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # def test_invalid_patch_student(self):
    #     # delete an existing student
    #     response = self.client.delete('/student/', {'id':'0ee814e2-5a93-43f8-965d-31b2a87a1d69'})
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(Student.objects.count(), 1)

    def test_patch_invalid_email_address(self):
        new_data = {'id':self.student.id, 'div': 'A', 'mail': 'invalid_email'}
        response = self.client.patch('/student/', new_data)
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertEqual(response.json(),{"status": "error", "error_code": 103, "message": "error: ['Enter a valid email address.']"})
   
    def test_patch_invalid_student(self):
        # create a new student without pass mobile key
        new_data = {'id':'0ee814e2-5a93-43f8-965d-31b2a87a1d69', 'name': 'Akshay', 'division': 'A', 'mail': 'akshaygupta@gmail.com'}
        response = self.client.patch('/student/',new_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_student(self):
        # delete an existing student
        response = self.client.delete('/student/', {'id':self.student.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)


    def test_invalid_delete_student(self):
        # delete an existing student
        response = self.client.delete('/student/', {'id':'0ee814e2-5a93-43f8-965d-31b2a87a1d69'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Student.objects.count(), 1)

    def test_wrongUUID_delete_student(self):
        # delete an existing student
        response = self.client.delete('/student/', {'id':'0ee814e2-5a93-43f8-965d-31b'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Student.objects.count(), 1)



