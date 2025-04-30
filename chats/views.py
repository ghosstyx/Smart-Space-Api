from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from .models import Chat, Message
from accounts.models import NaturalPerson
from django.urls import reverse


class ChatListView(ListView):
    model = Chat
    template_name = 'chats/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        self.current_user = get_object_or_404(NaturalPerson, id=self.kwargs['user_id'])
        return Chat.objects.filter(participants=self.current_user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.current_user
        context['other_users'] = NaturalPerson.objects.exclude(id=self.current_user.id)
        return context


class ChatDetailView(DetailView):
    model = Chat
    template_name = 'chats/chat_detail.html'
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        context['current_user'] = get_object_or_404(NaturalPerson, id=user_id)
        context['messages'] = self.object.messages.all().order_by('timestamp')
        return context

    def post(self, request, *args, **kwargs):
        chat = self.get_object()
        user_id = self.kwargs['user_id']
        current_user = get_object_or_404(NaturalPerson, id=user_id)
        text = request.POST.get('text', '').strip()

        if text:
            Message.objects.create(
                chat=chat,
                sender=current_user,
                text=text
            )

        return redirect(reverse('chats:chat_detail', kwargs={
            'user_id': user_id,
            'pk': chat.pk
        }))


class ChatCreateView(View):
    def post(self, request, user_id):
        current_user = get_object_or_404(NaturalPerson, id=user_id)
        other_user_id = request.POST.get('other')
        other_user = get_object_or_404(NaturalPerson, id=other_user_id)

        # Проверяем существующий чат
        existing_chat = Chat.objects.filter(participants=current_user) \
            .filter(participants=other_user).first()

        if existing_chat:
            return redirect(reverse('chats:chat_detail', kwargs={
                'user_id': user_id,
                'pk': existing_chat.pk
            }))

        # Создаем новый чат
        new_chat = Chat.objects.create()
        new_chat.participants.add(current_user, other_user)
        return redirect(reverse('chats:chat_detail', kwargs={
            'user_id': user_id,
            'pk': new_chat.pk
        }))