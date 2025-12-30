/**
 * Hours Edit Page JavaScript
 * Handles "Closed" checkbox functionality for business hours editing
 */

document.addEventListener('DOMContentLoaded', function() {
  // Get all closed toggle checkboxes
  const closedToggles = document.querySelectorAll('.day-closed-toggle');
  
  closedToggles.forEach(function(checkbox) {
    const day = checkbox.dataset.day;
    const timeInputsContainer = document.querySelector(`[data-day-inputs="${day}"]`);
    const openInput = document.getElementById(`id_${day}_open`);
    const closeInput = document.getElementById(`id_${day}_close`);
    
    // Check initial state - if both times are empty, check the closed box
    if (openInput && closeInput && !openInput.value && !closeInput.value) {
      checkbox.checked = true;
      timeInputsContainer.classList.add('disabled');
    }
    
    // Handle checkbox changes
    checkbox.addEventListener('change', function() {
      if (this.checked) {
        // Closed - clear and disable time inputs
        if (openInput) openInput.value = '';
        if (closeInput) closeInput.value = '';
        timeInputsContainer.classList.add('disabled');
      } else {
        // Open - enable time inputs
        timeInputsContainer.classList.remove('disabled');
      }
    });
  });
});