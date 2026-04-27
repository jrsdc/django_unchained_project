from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django import forms

@login_required
def inbox(request, msg_id=None):
    query = request.GET.get('q')
    messages = Message.objects.filter(recipient=request.user, is_draft=False).order_by('-timestamp')
    
    if query:
        messages = messages.filter(
            Q(subject__icontains=query) | 
            Q(body__icontains=query) | 
            Q(sender__username__icontains=query)
        )

    selected_message = None
    if msg_id:
        selected_message = get_object_or_404(Message, id=msg_id, recipient=request.user)
    elif messages.exists():
        selected_message = messages[0]
        
    return render(request, 'user_messages/inbox.html', {
        'messages': messages, 
        'selected_message': selected_message,
        'query': query
    })

@login_required
def sent_messages(request, msg_id=None):
    query = request.GET.get('q')
    messages = Message.objects.filter(sender=request.user, is_draft=False).order_by('-timestamp')
    
    if query:
        messages = messages.filter(
            Q(subject__icontains=query) | 
            Q(body__icontains=query) | 
            Q(recipient__username__icontains=query)
        )

    selected_message = None
    if msg_id:
        selected_message = get_object_or_404(Message, id=msg_id, sender=request.user)
    elif messages.exists():
        selected_message = messages[0]

    return render(request, 'user_messages/sent.html', {
        'messages': messages,
        'selected_message': selected_message,
        'query': query
    })

@login_required
def drafts(request, msg_id=None):
    query = request.GET.get('q')
    messages = Message.objects.filter(sender=request.user, is_draft=True).order_by('-timestamp')
    
    if query:
        messages = messages.filter(
            Q(subject__icontains=query) | 
            Q(body__icontains=query) | 
            Q(recipient__username__icontains=query)
        )

    selected_message = None
    if msg_id:
        selected_message = get_object_or_404(Message, id=msg_id, sender=request.user)
    elif messages.exists():
        selected_message = messages[0]

    return render(request, 'user_messages/drafts.html', {
        'messages': messages,
        'selected_message': selected_message,
        'query': query
    })

@login_required
def new_message(request, draft_id=None):
    users = User.objects.exclude(id=request.user.id)
    draft = None
    
    if draft_id:
        draft = get_object_or_404(Message, id=draft_id, sender=request.user, is_draft=True)

    if request.method == "POST":
        recipient_id = request.POST.get('recipient')
        recipient = get_object_or_404(User, id=recipient_id)
        is_draft_mode = 'save_draft' in request.POST
        
        if draft:
            draft.recipient = recipient
            draft.subject = request.POST.get('subject')
            draft.body = request.POST.get('body')
            draft.is_draft = is_draft_mode
            draft.save()
        else:
            Message.objects.create(
                sender=request.user,
                recipient=recipient,
                subject=request.POST.get('subject'),
                body=request.POST.get('body'),
                is_draft=is_draft_mode
            )
        
        return redirect('drafts' if is_draft_mode else 'sent_messages')
        
    return render(request, 'user_messages/new_message.html', {'users': users, 'draft': draft})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    was_draft = message.is_draft
    message.delete()
    
    if was_draft:
        return redirect('drafts')
    return redirect('sent_messages')

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'user_messages/register.html', {'form': form})

def dashboard(request):
    return render(request, 'user_messages/dashboard.html')

def teams_page(request):
    return render(request, 'user_messages/teams.html')

def settings_page(request):
    return render(request, 'user_messages/settings.html')