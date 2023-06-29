document.addEventListener('DOMContentLoaded', function() {
    const sortSelectDropdown = document.getElementById('sortSelect');
    sortSelectDropdown.addEventListener('change', function(event) {
      event.preventDefault(); // Prevent default form submission
      const selectedIndex = this.selectedIndex;
      const selectedOption = this.options[selectedIndex].value;
      console.log(selectedOption); // Debugging: Output the selected option value
      const currentUrl = new URL(window.location.href);
      currentUrl.searchParams.set('sort', selectedOption);
      window.location.href = currentUrl.toString();
    });
  });