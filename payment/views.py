from django.shortcuts import render, redirect, get_object_or_404
import braintree
from events.models import OrderTickets, EventTickets
from django.contrib.auth.decorators import login_required


@login_required
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(OrderTickets, id = order_id)

    if request.method == 'POST':
        # Get token
        nonce = request.POST.get('payment_method_nonce', None)
        
        # Creating and sending transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.total_price),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        # Success payment
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        # Payment not successful
        else:
            # Adding unpurchased tickets
            for ticket in order.order.all():
                event_ticket = get_object_or_404(EventTickets, id=ticket.event_ticket.id)
                event_ticket.number += ticket.quantity
                event_ticket.save()
            return redirect('payment:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        return render(request,
                      'payment/process.html',
                      {'order': order,
                      'client_token': client_token})

@login_required
def payment_done(request):
    return render(request, 'payment/done.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment/canceled.html')