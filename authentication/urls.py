from django.urls import path
from . import views

urlpatterns = [
    # ...

    path('', views.login_view, name='login'),
    path('forgotpasword',views.forgot_view,name='forgotpassword'),
    path('send_password_recovery_email/', views.send_password_recovery_email, name='recovery_email'),
    # ...
]
