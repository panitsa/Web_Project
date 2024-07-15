from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView 

class CustomLoginView(LoginView):
    template_name = 'admin/login.html'

class EditView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/edit.html'
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
