from django.urls import path,include
from . import views

urlpatterns = [

	path('create/',views.CreateUserView.as_view(),name="create"),
	path('login/',views.UserLoginView.as_view(),name="login"),
	path('update/',views.UserUpdateView.as_view(),name="update"),

]