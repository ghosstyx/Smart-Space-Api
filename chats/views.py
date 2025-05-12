from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Chat, Message
from accounts.models import NaturalPerson
from django.urls import reverse


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'chats/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['other_users'] = NaturalPerson.objects.exclude(pk=self.request.user.pk)
        return context


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chats/chat_detail.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['messages'] = self.object.messages.all().order_by('timestamp')
        return context

    def post(self, request, *args, **kwargs):
        chat = self.get_object()
        text = request.POST.get('text', '').strip()

        if text:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                text=text
            )

        return redirect(reverse('chats:chat_detail', kwargs={
            'pk': chat.pk
        }))


class ChatCreateView(LoginRequiredMixin, View):
    def post(self, request):
        other_user_pk = request.POST.get('other')
        other_user = get_object_or_404(NaturalPerson, pk=other_user_pk)

        # Проверяем существующий чат
        existing_chat = Chat.objects.filter(participants=request.user) \
            .filter(participants=other_user).first()

        if existing_chat:
            return redirect(reverse('chats:chat_detail', kwargs={
                'pk': existing_chat.pk
            }))

        # Создаем новый чат
        new_chat = Chat.objects.create()
        new_chat.participants.add(request.user, other_user)
        return redirect(reverse('chats:chat_detail', kwargs={
            'pk': new_chat.pk
        }))