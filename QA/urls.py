from django.urls import path
from . import views

app_name = 'QA'

urlpatterns = [
    path('ask/', views.ask_question, name='ask'),
    path('question/<int:question_id>/', views.question_detail, name='detail'),
    path('answer/<int:answer_id>/accept/', views.accept_answer, name='accept_answer'),
    path('answer/<int:answer_id>/like/', views.toggle_like_answer, name='toggle_like_answer'),
    path('answer/<int:answer_id>/comment/', views.post_answer_comment, name='post_comment'),
    path('question/all/',views.AllQuestionsListView,name='all')
]
