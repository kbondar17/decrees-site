from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from decrees import appointment_views 

app_name = 'decrees'

urlpatterns = [

    path('login/', appointment_views.MyLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='decrees:login'), name='logout'),

#     path('events/login', appointment_views.MyLogin.as_view(), name='event-login'),

    path('event-form/', appointment_views.EventView.as_view(), name='event-form'),
    path('event-form/create', appointment_views.AddEvent.as_view(), name='create-event'),
    
    path('event-form/<int:pk>', appointment_views.ShowOneEvent.as_view(), name='show-event'),
    
    # path('event-form/update/<int:pk>', appointment_views.EditEvent.as_view(), name='update-event'),
    re_path(r'^event-form/update/(?P<pk>[0-9]{1,999})/*', appointment_views.EditEvent.as_view(), name='update-event'),
    
    path('event-form/<int:pk>/delete', appointment_views.DeleteEvent.as_view(), name='delete-event'),

    path('events/', appointment_views.ShowAllEvents.as_view(), name='show-all-events'),
    path('events/<str:query>', appointment_views.ShowAllEvents.as_view(), name='show-all-events'),



]

# handler404 = decrees.views.error_404

# from django.conf.urls.static import static
# TODO# urlpatterns += static(settings.STAT)
