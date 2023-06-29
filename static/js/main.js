function sortBikes(sortOption) {
  const urlParams = new URLSearchParams(window.location.search);
  urlParams.set('sort', sortOption);
  window.location.href = window.location.pathname + '?' + urlParams.toString();
}

// Get the current sort option from the URL and set it as the selected option
const urlParams = new URLSearchParams(window.location.search);
const currentSortOption = urlParams.get('sort');
document.getElementById('sort').value = currentSortOption || 'manufacturer';