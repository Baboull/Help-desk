from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, InternalNote
from .forms import TicketCreateForm, TicketMessageForm
from chat.models import Message
from departments.models import Department

@login_required
def client_dashboard(request):
    tickets = Ticket.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'tickets/client_dashboard.html', {'tickets': tickets})

@login_required
def staff_dashboard(request):
    if request.user.role not in ['staff', 'admin'] and not request.user.is_staff:
        return redirect('client_dashboard')
    
    assigned_tickets = Ticket.objects.filter(assigned_to=request.user).order_by('-updated_at')
    unassigned_tickets = Ticket.objects.filter(assigned_to__isnull=True).order_by('-created_at')
    
    return render(request, 'tickets/staff_dashboard.html', {
        'assigned_tickets': assigned_tickets,
        'unassigned_tickets': unassigned_tickets
    })

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.client = request.user
            ticket.save()
            messages.success(request, 'Ticket created successfully.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketCreateForm()
    
    return render(request, 'tickets/ticket_create.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    is_staff = request.user.role in ['staff', 'admin'] or request.user.is_staff
    if not is_staff and ticket.client != request.user:
        return redirect('client_dashboard')

    if request.method == 'POST':
        if 'chat_message' in request.POST:
            form = TicketMessageForm(request.POST)
            if form.is_valid():
                msg = form.save(commit=False)
                msg.ticket = ticket
                msg.sender = request.user
                msg.save()
                return redirect('ticket_detail', ticket_id=ticket.id)
                
        elif 'update_status' in request.POST and is_staff:
            new_status = request.POST.get('status')
            if new_status in dict(Ticket.STATUS_CHOICES):
                ticket.status = new_status
                ticket.save()
                messages.success(request, f'Status updated to {ticket.get_status_display()}')
                return redirect('ticket_detail', ticket_id=ticket.id)
                
        elif 'claim_ticket' in request.POST and is_staff:
            ticket.assigned_to = request.user
            ticket.save()
            messages.success(request, 'You have claimed this ticket.')
            return redirect('ticket_detail', ticket_id=ticket.id)
            
        elif 'add_note' in request.POST and is_staff:
            note_content = request.POST.get('note_content')
            if note_content:
                InternalNote.objects.create(
                    ticket=ticket,
                    author=request.user,
                    note=note_content
                )
                messages.success(request, 'Internal note added.')
                return redirect('ticket_detail', ticket_id=ticket.id)

    chat_messages = ticket.messages.all().order_by('created_at')
    internal_notes = ticket.internal_notes.all().order_by('-created_at') if is_staff else []
    chat_form = TicketMessageForm()

    return render(request, 'tickets/ticket_detail.html', {
        'ticket': ticket,
        'chat_messages': chat_messages,
        'chat_form': chat_form,
        'is_staff': is_staff,
        'internal_notes': internal_notes,
    })

@login_required
def resolved_tickets(request):
    """Public archive: all resolved/closed tickets visible to every logged-in user."""
    query = request.GET.get('q', '').strip()
    qs = Ticket.objects.filter(status__in=['resolved', 'closed']).order_by('-updated_at')
    if query:
        qs = qs.filter(title__icontains=query) | qs.filter(description__icontains=query)
        qs = qs.distinct()
    return render(request, 'tickets/resolved_tickets.html', {
        'tickets': qs,
        'query': query,
    })
