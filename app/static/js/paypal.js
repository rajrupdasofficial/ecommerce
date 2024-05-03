//<script src="https://www.paypal.com/sdk/js?client-id=AT-9V4o_Ntnhs6TgvnfvTDbhVe3j4DHB11TYsY6DhZ5XEs2gpCKVPjyCLJiYo4katruRTE9x6yizxi7E&currency=USD"></script>

functioninitPayPalButton(){
paypal.Buttons({
style: {
shape: 'rect',
color: 'gold',
layout: 'vertical',
label: 'paypal',
},

createOrder:function(data,actions){
return actions.order.create({
purchase_units: [{"amount":{"currency_code": "USD", "value": '{{total_amount}}'}}]
});
},
onApprove:function(data,actions){
return actions.order.capture().then(function(orderData){
var paypalPaymentID = orderData.purchase_units[0].payments.captures[0].id;
// Full available details
console.log('Capture result', orderData, JSON.stringify(orderData, null, 2));
// Show a success message within this page, for example:
constelement= document.getElementById('paypal-button-container');
element.innerHTML = '';
element.innerHTML = '<h3>Thank you for your payment!</h3>';
document.getElementById('paypal-payment-id').value = paypalPaymentID;
document.getElementById('myform').submit();
// Or go to another URL: actions.redirect('thank_you.html');
});
},
onError:function(err){
console.log(err);
}
}).render('#paypal-button-container');
}
initPayPalButton();

