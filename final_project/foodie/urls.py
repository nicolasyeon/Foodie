from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('logout', views.logout),
    path('new_review/<int:user_id>', views.new_review),
    path('create_review/<int:user_id>', views.create_review),
    path('view_review/<int:review_id>', views.view_review),
    path('edit_review/<int:review_id>', views.edit_review),
    path('remove_review/<int:review_id>', views.remove_review),
    path('view_account/<int:user_id>', views.view_account),
    path('edit_account/<int:user_id>', views.edit_account),
    path('like/<int:review_id>', views.like),
    path('unlike/<int:review_id>', views.unlike),
    path('list_restaurants', views.list_restaurants),
    path('current_location', views.current_location)
]
