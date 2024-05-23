from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from student.models import Student
from supervisor.models import Supervisor
from chat.models import Conversation, Message

def show_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, pk=conversation_id)
    supervisor = conversation.supervisor
    unit_co = conversation.unit_co
    group = conversation.group
    other_members_of_group = []
    if group is not None and group.user_set:
        other_members_of_group = group.user_set.exclude(username=request.user.username)
    messages = Message.objects.filter(conversation=conversation)
    permitted_users = [supervisor.user]
    if unit_co is not None:
        permitted_users.append(unit_co.user)
    if group is not None:
        permitted_users.extend(group.user_set.all())

    # Add the current user to the read_users field of the conversation
    conversation.read_users.add(request.user)

    if request.method == 'POST':
        message_text = request.POST.get('message')
        message = Message.objects.create(
            user=request.user,
            conversation=conversation,
            message=message_text
        )
        message.save()
        return redirect('conversation', conversation_id=conversation_id)
    else:
      return render(request, 'show_conversation.html', {
          'conversation': conversation,
          'conversation_title': conversation.conversation_title,
          'supervisor': supervisor,
          'unit_co': unit_co,
          'group': group,
          'other_members_of_group': other_members_of_group,
          'messages': messages,
          'permitted_users': permitted_users,
      })