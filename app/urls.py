from django.urls import path

from . import views

urlpatterns = [

    path('', view=views.AppsAPIView.as_view(), name='apps'),
    path('create', view=views.AppAPIView.as_view(), name='create'),
    path('<int:app_id>', view=views.AppAPIView.as_view(), name='app'),
    path('<int:app_id>/history', view=views.AppHistoryAPIView.as_view(), name='history'),
    path('<int:app_id>/run', view=views.AppRunAPIView.as_view(), name='run')

]
