from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_employer:
            return redirect('employers:employer_dashboard')
        else:
            return redirect('jobseekers:jobseeker_dashboard')
    return render(request, 'jobseeking/home.html')