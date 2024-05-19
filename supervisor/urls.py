from django.urls import path
from . import views
from unit_co import views as unit_co_views

urlpatterns = [
    path('my_projects/', views.my_projects, name='my_projects'),
    path('create_project/', views.create_project, name='create_project'),
    # path('applications/', views.applications, name='applications'),
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('applications/', unit_co_views.applications, name='applications_supervisor'),
    path('view_application/<int:application_id>/', unit_co_views.view_application, name='view_application_supervisor'),
    path('delete_application/<int:application_id>/', unit_co_views.delete_application, name='delete_application_supervisor'),
    path('approve_application/<int:application_id>/', unit_co_views.approve_application, name='approve_application_supervisor'),
    path('reject_application/<int:application_id>/', unit_co_views.reject_application, name='reject_application_supervisor'),
]
