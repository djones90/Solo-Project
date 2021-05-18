from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
path('', views.home),
path('register', views.register),
path('login', views.login),
path('success', views.success),
path('new', views.new),
path('create', views.create),
path('<int:post_id>/edit', views.edit),
path('<int:post_id>/update', views.update),
path('<int:post_id>/delete', views.delete),
path('<int:post_id>', views.post_details),
path('<int:post_id>/comment', views.comment),
path('logout', views.logout),
]