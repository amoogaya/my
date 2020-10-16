from django.urls import path
from . import views

app_name='polls'
urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
    path('<int:pk>/',views.DetailedView.as_view(),name='detailed'),
    path('<int:pk>/results/',views.Result.as_view(),name='results'),
    path('<int:question_id>/votes/',views.votes,name='votes'),
]
