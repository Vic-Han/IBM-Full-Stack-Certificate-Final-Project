from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    #default route
    path(route = '', view = views.home, name = 'home'),
    # path for about view
    path(route = 'about/<str:username>/<str:status>', view = views.about, name = 'about'),
    # path for contact us view
    path(route = 'contact/<str:username>/<str:status>', view = views.contact, name = 'contact'),
    # path for registration
    path(route = 'registerpage' , view = views.registerpage, name = 'registerpage'),

    path(route = 'registration', view = views.registration_request, name = 'registration'),
    # path for login
    path(route = 'login', view = views.login_view, name = 'login'),
    # path for logout
    path(route = 'logout', view = views.logout_request, name = 'logout'),

    path(route='home/<str:username>/<str:status>', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer/<str:username>/<str:status>/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),
    # path for add a review view
    path(route='add_review/<str:username>/<str:status>/<int:dealer_id>', view=views.add_review, name='add_review'),
    # path for post a review view
    path(route='dealers/<str:username>/<str:status>/<int:dealer_id>', view=views.post_review, name='post_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)