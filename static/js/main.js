$('.toast').toast('show');

function sortBikes(sortOption) {
  var urlParams = new URLSearchParams(window.location.search);
  urlParams.set('sort', sortOption);
  window.location.href = window.location.pathname + '?' + urlParams.toString();
}

// Get the current sort option from the URL and set it as the selected option
const sortElement = document.getElementById('sort');

if (sortElement) {
  // The element exists, proceed with the code
  var urlParams = new URLSearchParams(window.location.search);
  var currentSortOption = urlParams.get('sort');
  sortElement.value = currentSortOption || 'manufacturer';
}

// Function for collapse of category nav items 
$(document).ready(function() {
  $('.collapse').on('show.bs.collapse', function() {
    $('.collapse.show').collapse('hide');
  });
});

// Function for quantity adjuster
$(document).ready(function() {
  $('.quantity-button').click(function() {
    var input = $(this).siblings('input');
    var value = parseInt(input.val());
    var step = parseInt(input.attr('step')) || 1;
    
    if ($(this).hasClass('minus')) {
      value = Math.max(value - step, 0);
    } else if ($(this).hasClass('plus')) {
      value += step;
    }
    
    input.val(value);
  });
});
