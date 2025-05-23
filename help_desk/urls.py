from django.urls import path
from .views import KanbanBoardView, ProjectCreateView, ProjectUpdateView

app_name = 'help_desk'

urlpatterns = [
    path('board/np-<int:np_id>/project-<int:pk>/', KanbanBoardView.as_view(), name='kanban_board'),
    path('project/create/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
]