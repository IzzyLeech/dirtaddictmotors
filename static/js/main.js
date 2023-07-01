function sortBikes(sortOption) {
  const urlParams = new URLSearchParams(window.location.search);
  urlParams.set('sort', sortOption);
  window.location.href = window.location.pathname + '?' + urlParams.toString();
}

// Get the current sort option from the URL and set it as the selected option
const sortElement = document.getElementById('sort');

if (sortElement) {
  // The element exists, proceed with the code
  const urlParams = new URLSearchParams(window.location.search);
  const currentSortOption = urlParams.get('sort');
  sortElement.value = currentSortOption || 'manufacturer';
}

$(document).ready(function() {
  $('.underline-link').click(function() {
    $(this).addClass('clicked-link');
  });
});
