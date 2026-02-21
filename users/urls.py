from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.profile_settings, name="profile_settings"),
    path("admin-management/", views.admin_management, name="admin_management"),
    path(
        "admin-management/user/<int:user_id>/",
        views.admin_user_edit,
        name="admin_user_edit",
    ),
]
