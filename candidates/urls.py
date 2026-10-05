from django.urls import path
from . import views

urlpatterns = [

    path(
        'upload/',
        views.upload_candidates,
        name='upload_candidates'
    ),

    path(
        '',
        views.candidate_list,
        name='candidate_list'
    ),

    path(
    '<int:candidate_id>/screen/',
    views.screen_candidate,
    name='screen_candidate'
),

]