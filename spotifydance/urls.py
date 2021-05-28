from django.urls import path
from . import views

urlpatterns = [
    #path('', views.dancer, name='dancer'),
    path('viewer/', views.viewer, name='viewer'),
 path('', views.start, name='start'),
 path('safari/', views.safari, name='safari'),
  path('land/', views.land, name='land'),
  path('empty_search/', views.empty_search, name='empty_search'),
    path('viewer2/', views.viewer2, name='viewer2'),
      path('land2/', views.land2, name='land2'),
          path('viewer3/', views.viewer3, name='viewer3'),
      path('land3/', views.land3, name='land3'),
                path('viewer4/', views.viewer4, name='viewer4'),
      path('land4/', views.land4, name='land4'),
                      path('viewer5/', views.viewer5, name='viewer5'),
      path('land5/', views.land5, name='land5'),


]

