from django.core.mail import message
from Job_Seeking_App.views import *
from django.test import TestCase
from .models import *

# Create your tests here.
class UserTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.user = User(id=1,username='NickMoringa',email= 'nick@moringa.com',first_name='Nicholas',last_name='Ngetich',phone='254725470732',is_jobseeker=True)
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def tearDown(self):
        self.user.delete_user()

    def test_save_method(self):
        self.user.save_user()
        users  = User.objects.all()
        self.assertTrue(len(users)>0)

    def test_get_all_users(self):
        users = User.get_all_users()
        self.assertTrue(len(users)>0)

    def test_get_user_id(self):
        users= User.get_user_id(self.user.id)
        self.assertTrue(len(users) == 1)

def test_update_user(self):
        self.user.save_user()
        user = User.update_user( self.user.id, 'Nick@Moringa','nick@moringa.com','Nick','Korgoren','254725470732',True)
        user_item = user.objects.filter(id = self.user.id)
        print(user_item)
        self.assertTrue(user.name == 'Nick@Moringa')


class FileUploadTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.user = User(id=1,username='Nick',email='nick@gmail.com',bio='',)
        self.user.save_user()

        self.upload = FileUpload(name='Home upload', pdf='pdf.url',user= self.user)
        self.upload.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.upload, FileUpload))

    def tearDown(self):
        self.upload.delete_upload()

    def test_save_method(self):
        self.upload.save_upload()
        uploads  = FileUpload.objects.all()
        self.assertTrue(len(uploads)>0)

    def test_get_all_uploads(self):
        uploads = FileUpload.get_all_uploads()
        self.assertTrue(len(uploads)>0)

    def test_get_upload_id(self):
        uploads= FileUpload.get_upload_id(self.upload.id)
        self.assertTrue(len(uploads) == 1)

def test_update_upload(self):
        self.upload.save_upload()
        upload = FileUpload.update_upload( self.upload.id, 'test update', 'my test')
        upload_item = upload.objects.filter(id = self.upload.id)
        print(upload_item)
        self.assertTrue(upload.name == 'test update')


class PortfolioTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.user = User(id=2,username='Moringa',email='moringa@gmail.com',bio='',)
        self.user.save_user()

        self.portfolio = Portfolio(name='CV', link='moringa_portfolio.com',user= self.user)
        self.portfolio.save()


    def test_instance(self):
        self.assertTrue(isinstance(self.portfolio, Portfolio))

    def tearDown(self):
        self.portfolio.delete_portfolio()

    def test_save_method(self):
        self.portfolio.save_portfolio()
        portfolios  = Portfolio.objects.all()
        self.assertTrue(len(portfolios)>0)

    def test_get_all_portfolios(self):
        portfolios = Portfolio.get_all_portfolios()
        self.assertTrue(len(portfolios)>0)

    def test_get_portfolio_id(self):
        portfolios= Portfolio.get_portfolio_id(self.portfolio.id)
        self.assertTrue(len(portfolios) == 1)

def test_update_portfolio(self):
        self.portfolio.save_portfolio()
        portfolio = Portfolio.update_portfolio( self.portfolio.id, 'test update', 'portfolio test')
        portfolio_item = portfolio.objects.filter(id = self.portfolio.id)
        print(portfolio_item)
        self.assertTrue(portfolio.name == 'test update')

class ContactTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.contact = Contact(name='Paul Jeoffrey', email='pauljeff@gmail.com',message= 'Hello Flex-Connectors, how long will it take to verify my employer account once I make the payment')
        self.contact.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.contact, Contact))

    def tearDown(self):
        self.contact.delete_contact()

    def test_save_method(self):
        self.contact.save_contact()
        contacts  = Contact.objects.all()
        self.assertTrue(len(contacts)>0)

    def test_get_all_contacts(self):
        contacts = Contact.get_all_contacts()
        self.assertTrue(len(contacts)>0)

    def test_get_contact_id(self):
        contacts= Contact.get_contact_id(self.contact.id)
        self.assertTrue(len(contacts) == 1)


class PaymentDetailsTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.payment = Payments(id=3,first_name='Nicholas',last_name='Ngetich',phone='254725470732',)
        self.payment.save()
 
