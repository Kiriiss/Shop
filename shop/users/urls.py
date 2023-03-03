from django.urls import path

from users.views import logout_view, signup, user_login, password_reset_request, profile, delete_from_cart, elit_profile

app_name = 'users'

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('reset-password/', password_reset_request, name="password_reset"),
    path('user_profile/', profile, name='profile'),
    path('delete_from_cart/<int:basket_id>/', delete_from_cart, name='delete_from_cart'),
    path('edit_profile/', elit_profile, name='edit_profile'),
]
