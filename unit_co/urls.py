from django.urls import path
from . import views
from supervisor.views import edit_project as edit_project_su, delete_project as delete_project_su

urlpatterns = [
  path('edit_project/<int:project_id>/', edit_project_su, name='edit_project_unit_co'),
  path('delete_project/<int:project_id>/', delete_project_su, name='delete_project_unit_co'),
  path('pending_projects/', views.pending_projects, name='pending_projects'),
]