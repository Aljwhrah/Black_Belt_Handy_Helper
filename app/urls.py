from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('dashboard', views.show_job),  
    path('dashboard/edit/dashboard', views.show_job),  
    path('register', views.register_user),
    path('login', views.login_user),
    path('logout', views.logout_user),
    path('dashboard/create', views.create_job),
    path('jobs/new', views.detaile),
    path('jobs/edit/<int:id>', views.edit),
    path('jobs/grant/<int:id>', views.grant),
    path('jobs/ungrant/<int:id>', views.ungrant),

    path('jobs/grant_show/<int:id>', views.grant_show),
    path('jobs/ungrant_show/<int:id>', views.ungrant_show),
    path('jobs/show/<int:id>', views.detaile),
    path('dashboard/<int:id>/delete', views.job_destroy),
    path('dashboard/<int:id>/update', views.job_update),
    path('jobs/<int:id>', views.shows)

]