from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("tanks_info/", views.tanks_info, name="tanks_info"),
    path('favorite/gun/add/<int:gun_id>/', views.add_favorite_gun, name='add_favorite_gun'),
    path('favorite/gun/remove/<int:gun_id>/', views.remove_favorite_gun, name='remove_favorite_gun'),
    path('favorite/body/add/<int:body_id>/', views.add_favorite_body, name='add_favorite_body'),
    path('favorite/body/remove/<int:body_id>/', views.remove_favorite_body, name='remove_favorite_body'),
    path('favorites/', views.favorites_view, name='favorites'),

]
