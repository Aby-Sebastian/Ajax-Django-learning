from django.urls import path
from . import views

urlpatterns = [
	
	path('',views.links, name="links"),
	path('save/',views.save_data, name="save"),
	path('edit/',views.edit_links, name="edit"),
	path('delete/',views.delete, name="delete"),
	path('page/<str:pk>',views.pages, name="pages"),
]
