/**
 * Calendar - Upcoming Events Progressive Loading
 * Handles "Load More" functionality for upcoming events section
 */

document.addEventListener('DOMContentLoaded', function() {
  const loadMoreBtn = document.getElementById('load-more-events-btn');
  
  if (!loadMoreBtn) {
    return; // Exit if button doesn't exist
  }
  
  let currentlyShowing = 3;
  const eventsPerLoad = 3;
  const eventItems = document.querySelectorAll('.upcoming-event-item');
  const totalEvents = eventItems.length;
  
  loadMoreBtn.addEventListener('click', function() {
    // Show next 3 events
    let showCount = 0;
    for (let i = currentlyShowing; i < eventItems.length && showCount < eventsPerLoad; i++) {
      eventItems[i].classList.remove('event-hidden');
      showCount++;
    }
    
    currentlyShowing += showCount;
    
    // Hide button if all events are shown
    if (currentlyShowing >= totalEvents) {
      loadMoreBtn.style.display = 'none';
    }
  });
});