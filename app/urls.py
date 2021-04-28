from django.urls import path
from . import views

urlpatterns = [
	path('',views.index,name='index'),
	path('login/',views.login, name='login'),
	path('register/',views.register,name='register'),
	path('dashboard/',views.dashboard, name="dashboard"),
	path('links/',views.links, name="links"),
	path('save/',views.save_data, name="save"),
	path('edit/',views.edit_links, name="edit"),
	path('delete/',views.delete, name="delete"),
]