# context_processors.py

from .functions import fetch_conversations

def conversations_processor(request):
    conversations, new_conversations_count = fetch_conversations(request)
    return {'conversations': conversations, 'new_conversations_count': new_conversations_count}