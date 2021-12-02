from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register_page', views.register_page),
    path('register', views.register),
    path('login_page', views.login_page),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('explore', views.explore),
    path('collage_page', views.collage_page),
    path('discover_collage_page', views.discover_collage_page),
    path('create_collage_page', views.create_collage_page),
    path('create_collage/<int:user_id>', views.collage_page),
    path('logout', views.logout),
    path('view_review/<int:review_id>', views.view_review),
    path('edit_review/<int:review_id>', views.edit_review),
    path('remove_review/<int:review_id>', views.remove_review),
    path('view_account/<int:user_id>', views.view_account),
    path('edit_account/<int:user_id>', views.edit_account),
    path('like/<int:review_id>', views.like),
    path('unlike/<int:review_id>', views.unlike),
    path('list_restaurants', views.list_restaurants),
    path('select_category', views.select_category),
    path('current_location', views.current_location)
]
