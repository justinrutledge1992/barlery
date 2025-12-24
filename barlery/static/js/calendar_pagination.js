// Calendar page - AJAX pagination for events
document.addEventListener('DOMContentLoaded', function() {
  const loadMoreBtn = document.getElementById('load-more-btn');
  const eventsGrid = document.getElementById('events-grid');
  
  if (!loadMoreBtn || !eventsGrid) {
    return; // Exit if elements don't exist
  }
  
  loadMoreBtn.addEventListener('click', function() {
    const page = parseInt(this.getAttribute('data-page'));
    
    // Disable button and show loading state
    loadMoreBtn.disabled = true;
    loadMoreBtn.classList.add('loading');
    loadMoreBtn.textContent = 'Loading...';
    
    // Make AJAX request
    fetch(`?page=${page}`, {
      method: 'GET',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
    .then(response => response.json())
    .then(data => {
      // Create temporary container for new HTML
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = data.html;
      
      // Append each new event card to the grid
      while (tempDiv.firstChild) {
        eventsGrid.appendChild(tempDiv.firstChild);
      }
      
      // Update button state
      if (data.has_more) {
        loadMoreBtn.setAttribute('data-page', data.next_page);
        loadMoreBtn.disabled = false;
        loadMoreBtn.classList.remove('loading');
        loadMoreBtn.textContent = 'Load More Events';
      } else {
        // No more events, remove the button
        loadMoreBtn.parentElement.remove();
      }
    })
    .catch(error => {
      console.error('Error loading more events:', error);
      loadMoreBtn.disabled = false;
      loadMoreBtn.classList.remove('loading');
      loadMoreBtn.textContent = 'Load More Events';
      alert('Error loading more events. Please try again.');
    });
  });
});