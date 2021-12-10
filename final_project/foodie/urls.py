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
    path('create_collage_page/<int:user_id>', views.create_collage_page),
    path('create_collage/<int:user_id>', views.create_collage),
    path('remove_collage/<int:collage_id>', views.remove_collage),
    path('add_to_collage/<str:business_id>', views.add_to_collage),
    path('add_restaurant/<int:collage_id>/<int:restaurant_id>', views.add_restaurant),
    path('collage_detail/<int:collage_id>', views.collage_detail),
    path('remove_restaurant/<int:collage_id>/<int:restaurant_id>', views.remove_restaurant),
    path('logout', views.logout),
    path('view_account/<int:user_id>', views.view_account),
    path('edit_account/<int:user_id>', views.edit_account),
    path('list_restaurants', views.list_restaurants),
    path('select_category', views.select_category),
    path('current_location_index', views.current_location_index),
    path('current_location_list_of_restaurants', views.current_location_list_of_restaurants)
]
