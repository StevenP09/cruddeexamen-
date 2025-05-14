from django.urls import include, path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('create/', prestamo_create, name='create'),
    path('list/', prestamo_list, name='list'),
    path('update/<int:id>', prestamo_update, name='update'),
    path('delete/<int:id>', prestamo_delete, name='delete'),
    path('get_tipoPrestamo/<int:id>', get_tipoPrestamo, name='get_tipoPrestamo'),
]

