from django.test import TestCase
from .models import JobSeeker
from django.contrib.auth.models import User

# Create your tests here.
class JobSeekerTest(TestCase):
    
  def setUp(self):
    self.user = User.objects.create(id=1, username='Roney-juma')
