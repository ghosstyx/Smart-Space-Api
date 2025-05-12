from django.urls import path
from .views import ChatListView, ChatDetailView, ChatCreateView

app_name = 'chats'

urlpatterns = [
    path('', ChatListView.as_view(), name='chat_list'),
    path('create/', ChatCreateView.as_view(), name='chat_create'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
]