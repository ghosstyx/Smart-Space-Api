from django.urls import path
from .views import ChatListView, ChatDetailView, ChatCreateView

app_name = 'chats'

urlpatterns = [
    path('<int:user_id>/', ChatListView.as_view(), name='chat_list'),
    path('<int:user_id>/create/', ChatCreateView.as_view(), name='chat_create'),
    path('<int:user_id>/chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
]