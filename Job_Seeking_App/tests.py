from _typeshed import Self
from Job_Seeking_App.apps import JobSeekingAppConfig
from django.test import TestCase
from .models import Portfolio,Employer,User,JobSeeker

# class PortfolioTestCase(TestCase):
#     def tearDown(self):
#         Portfolio.objects.all().delete()
#         JobSeeker.objects.all().delete()
#         Employer.objects.all().delete()

#     def setUp(self):
#         self.user = User(
#         first_name="Jane",
#         last_name="Doe",
#         email="jane@gmail.com",
#         location="langata",
#         phone="1236",
#         username='TestOne',
#         password='tests')
#         # save user instance
#         self.user.save()
#         # get jobseeker
#         # portfolio
#         self.portfolio = Portfolio(jobseeker=self.user,name="port",link='http://google.com')
#         self.portfolio.save()
        
#         # test instance
#     def test_instance(self):
#         self.assertTrue(isinstance(self.portfolio, Portfolio))

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
#         Self.assertEqual(post.title'title')
