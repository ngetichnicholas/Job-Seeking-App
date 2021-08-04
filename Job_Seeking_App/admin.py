from Job_Seeking_App.models import Employer, JobSeeker, Jobs, User,Category
from django.contrib import admin

# Register your models here.
admin.site.register(JobSeeker)
admin.site.register(Employer)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Jobs)
