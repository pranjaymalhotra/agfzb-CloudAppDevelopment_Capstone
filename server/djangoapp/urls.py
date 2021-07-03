from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    #path(route='static_page', view=views.simple_django_view, name='static_page'),

    path(route='about', view=views.get_about, name='about'),
    path(route='contact', view=views.get_contact, name='contact'),
    # path for registration
    
    path(route='login', view=views.get_login, name='login'),
    path(route='logout', view=views.get_logout, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),
    path(route='registration', view=views.registration_request, name='registration'),
    path(route='signup_view', view=views.signup_view, name='signup_view'),
    #path ( 'dealer/<int:dealer_id>/', views.get_dealer_details, name='dealer_details' ),
    #path ( 'r_eview/<int:rev_id>', views.add_review, name="add_review" ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)