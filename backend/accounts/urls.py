from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"   


urlpatterns = [
     path('logout/',
          auth_views.LogoutView.as_view(), name='logout'),
     path('login/',
          auth_views.LoginView.as_view(
               redirect_authenticated_user=True), name='login'),

     # path('password_reset/',
     #      views.password_reset_options, name='password_reset_options'),

     # password reset with email
     path('password_reset/', 
          auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
          name='password_reset'),
     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),
     path('password_reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')),
          name='password_reset_confirm'),
     path('password_reset/complete/',
          auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),

    # Registration
    # path('vendor/signup/', views.vendor_signup, name='vendor_signup'),
    # path('customer/signup/', views.customer_signup, name='customer_signup'),

     # path("register", views.register_request, name="register"),
     # path("login", views.login_request, name="login"),
     # path("logout", views.logout_request, name= "logout"),
<<<<<<< HEAD
>>>>>>> 632c1b53797fdcb26614ed3a36944f4accf851b7
=======
>>>>>>> 632c1b53797fdcb26614ed3a36944f4accf851b7
        
]
