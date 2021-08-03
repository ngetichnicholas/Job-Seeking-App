
from django.urls import include, path

from .views import jobseeking, jobseeker, employer

urlpatterns = [
    path('', jobseeking.home, name='home'),

    path('jobseeker/', include(([
        path('', jobseeker.JobSeekerDashboardView, name='jobseeker_dashboard'),
    ], 'jobseeking'), namespace='jobseeker')),

    path('employer/', include(([
        path('', employer.EmployerDashboardView, name='employer_dashboard'),
    ], 'jobseeking'), namespace='employer')),
]
