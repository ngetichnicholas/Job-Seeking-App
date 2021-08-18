from Job_Seeking_App.views import *
from django.test import TestCase
from .models import *

# Create your tests here.
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


class FileUploadTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.jobseeker = JobSeeker(bio='',user_id = 4)
        self.jobseeker.save_jobseeker()

        self.upload = FileUpload(name='Home upload', pdf='pdf.url',jobseeker= self.jobseeker)
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


class UserTestCase(TestCase):
  def setUp(self):
    
    
 