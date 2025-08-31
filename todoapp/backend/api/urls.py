from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.TodoListCreate.as_view(), name='todo_list'),
    path('todos/<int:pk>', views.TodoRetrieveUpdateDestroy.as_view(), name='todo_RUD'),
    path('todos/<int:pk>/complete', views.TodoToggleComplete.as_view()),
    path('signup/', views.signup, name='signup'), # Nueva ruta para registro
    path('login/', views.login, name='login'),   # Nueva ruta para login
]