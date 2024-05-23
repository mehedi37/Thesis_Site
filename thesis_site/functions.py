from django.contrib.auth.decorators import login_required
from chat.models import Conversation, Message
from django.db.models import Exists, OuterRef


# @login_required
def fetch_conversations(request):
  if request.user.is_authenticated and not request.user.is_superuser:
    # Fetch all conversations where the logged in user is a member
    conversations = Conversation.objects.filter(group__user=request.user).annotate(
        has_new_message=~Exists(
            Conversation.read_users.through.objects.filter(
                conversation_id=OuterRef('pk'),
                user_id=request.user.id
            )
        )
    )

    # Count the number of new conversations
    new_conversations_count = conversations.filter(has_new_message=True).count()

    for conversation in conversations:
        conversation.all_message = fetch_messages_from_conversation(request, conversation.conversation_id)
        conversation.title = conversation.group.name + " - " + conversation.supervisor.user.username
    return conversations, new_conversations_count
  else:
    return None, None

# @login_required
def fetch_messages_from_conversation(request, conversation_id):
    # Fetch all messages from a specific conversation
    messages = Message.objects.filter(conversation__conversation_id=conversation_id)
    return messages