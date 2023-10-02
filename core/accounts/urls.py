from django.urls import path
from .views import RegisterUserView, UserLoginView, UserLogoutView, test_func_celery, send_mail_to_all

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('celery-test/', test_func_celery, name='celery-test-func'),
    path('celery-email-test/', send_mail_to_all, name='celery-email-test-func'),

]
