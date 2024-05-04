# from django.shortcuts import render
# import stripe


# def checkout(request):
#     if request.method == 'POST':
#         amount = int(request.POST['amount']) * 100  # Convert to cents
#         session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[{
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': 'Your Product',
#                     },
#                     'unit_amount': amount,
#                 },
#                 'quantity': 1,
#             }],
#             mode='payment',
#             success_url='https://yourdomain.com/success/',
#             cancel_url='https://yourdomain.com/cancel/',
#         )
#         return render(request, 'checkout.html', {'session_id': session.id})
#     return render(request, 'checkout_form.html')
