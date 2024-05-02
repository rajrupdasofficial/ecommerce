
const src="https://js.stripe.com/v3/"

  var stripe = Stripe('{{ STRIPE_PUBLIC_KEY }}');
  stripe.redirectToCheckout({
    sessionId: '{{ session_id }}'
  }).then(function (result) {
    // If redirection fails, display an error to the customer
    if (result.error) {
      var displayError = document.getElementById('error-message');
      displayError.textContent = result.error.message;
    }
  });

