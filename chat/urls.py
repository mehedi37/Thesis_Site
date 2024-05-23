from django.urls import path
from . import views

urlpatterns = [
    path('view/<int:conversation_id>/', views.show_conversation, name='conversation'),
]
