var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripe_public_key);
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
var cardElement = elements.create('card', {style: style});
cardElement.mount('#card-element')


cardElement.addEventListener('change', function(event) {
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
    // Clear error message
    cardErrors.textContent = '';
    }
});

