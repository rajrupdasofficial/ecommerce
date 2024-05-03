def payment_done(request):


user = request.user
paypal_transaction_id = request.GET.get("paypal-payment-id")
custid = request.GET.get("custid")
customer = Customer.objects.get(id=custid)
cart_items = Cart.objects.filter(user=user)
# Check if the payment was made with PayPal
if paypal_transaction_id:
for cart in cart_items:
OrderPlaced.objects.create(
    user=user,
    customer=customer,
    product=cart.product,
    quantity=cart.quantity,
    transaction_id=paypal_transaction_id,
)
cart.delete()
return redirect("orders")
# Handle the case where PayPal payment ID is not provided
else:
return HttpResponse("Invalid payment information").
