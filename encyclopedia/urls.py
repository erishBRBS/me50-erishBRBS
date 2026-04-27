from django.urls import path, re_path
from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('new', views.new_page, name='new_page'),
    path('random', views.random_page, name='random_page'),
    path('edit/<str:title>', views.edit_page, name='edit_page'),
    path('wiki/<str:title>', views.entry, name='entry'),

    re_path(r'^.*$', views.route_not_found, name='route_not_found'),
]
