from django.urls import path

from user import views


app_name = "user"

urlpatterns = [
    path("createemployee/", views.CreateEmployeeView.as_view(),
         name="createemployee"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("employee/", views.ManageEmployeeView.as_view(), name="employee"),
    path("createrestaurant/", views.CreateRestaurantView.as_view(),
         name="createrestaurant"),
    path("restaurant/", views.ManageRestaurantView.as_view(),
         name="restaurant"),
]
