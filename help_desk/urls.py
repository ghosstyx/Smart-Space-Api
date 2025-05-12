from django.urls import path
from .views import KanbanBoardView

app_name = 'help_desk'

urlpatterns = [
    path('board/np-<int:np_id>/project-<int:pk>/', KanbanBoardView.as_view(), name='kanban_board'),
]