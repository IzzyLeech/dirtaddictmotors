var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Kanit", Kanit, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', { style: style });
card.mount('#card-element');
  
  // Handle card element change event
  card.addEventListener('change', function (event) {
    var cardErrors = document.getElementById('card-errors');
    if (event.error) {
      var html = `
        <span class="icon" role="alert">
          <i class="fas fa-exclamation-triangle"></i>
        </span>
        <span>${event.error.message}</span>
      `;
      $(cardErrors).html(html);
    } else {
      cardErrors.textContent = '';
    }
  });

// Handle form submission
var form = document.getElementById('checkout-form');
form.addEventListener('submit', function(event) {
    event.preventDefault();
    card.update({ 'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#checkout-form').fadeToggle(100);
    $('#loading-screen').fadeToggle(100);
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
          card: card,
      }
    }).then(function(result) {
        if (result.error) {
        console.error(result.error);
        var cardErrors = document.getElementById('card-errors');
        var html = `
            <span class="icon" role="alert">
            <i class="fas fa-exclamation-triangle"></i>
            </span>
            <span>${result.error.message}</span>
            `;
          $(cardErrors).html(html);
          $('#checkout-form').fadeToggle(100);
          $('#loading-screen').fadeToggle(100);
          card.update({ 'disabled': false});
          $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
            form.submit();
            }
        }
    });
});

