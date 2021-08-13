from os import name
from django.test import TestCase
from .models import *


class PortfolioTest(TestCase):
  def setUp(self):
    self.user = User.objects.create(id=1, username='salome')
    self.fileupload = Portfolio.objects.create(id=1, name='portfolio')

  def test_instance(self):
    self.assertTrue(isinstance(self.portfolio, Portfolio))

  def test_display_portfolio(self):
    self.portfolio.save()
    portfolio = Portfolio.all_portfolio()
    self.assertTrue(len(portfolio) > 0)

  def test_save_portfolio(self):
    self.portfolio.save_portfolio()
    portfolio = Portfolio.objects.all()
    self.assertTrue(len(portfolio) > 0)

class FileUploadTest(TestCase):
  def setUp(self):
    self.user = User.objects.create(id=1, username='salome')
    self.fileupload = FileUpload.objects.create(id=1,fileupload='fileupload')

  def test_instance(self):
    self.assertTrue(isinstance(self.fileupload, FileUpload))
    fileupload = FileUpload.objects.all()
    self.assertTrue(len(fileupload) > 0)

  def test_save_fileupload(self):
    self.fileupload.save_fileupload()
    fileupload = FileUpload.objects.all()
    self.assertTrue(len(fileupload) > 0)

class EmployerTestCase(TestCase):
    def setUp(self):
        self.user = User(
        first_name="John",
        last_name="Doe",
        email="john@gmail.com",
        location="compton",
        phone="123",
        username='Test',
        password='test')

        self.user.save()
<<<<<<< HEAD
        
        self.employer=Employer(user=self.user,company_name="TestLtd")
        self.employer.save_employer()
    # test instance
    def test_instance(self):
        self.assertTrue(isinstance(self.employer, Employer))


# Create your tests here.
# class UserTestClass(TestCase):
#     def setUp(self):
#         post_object.create(title='test', content='something')


#     def test_post_title{self}:
#         post=post.objects.get{id=4}
#         Self.assertEqual(post.title "title")
=======
 
>>>>>>> fd9efb01fc3cb4ad34a5fe8c0bf4ff4eeada75ac
