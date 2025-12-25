// Handle logout link click
document.addEventListener('DOMContentLoaded', function() {
  const logoutLink = document.getElementById('logout-link');
  const logoutForm = document.getElementById('logout-form');
  
  if (logoutLink && logoutForm) {
    logoutLink.addEventListener('click', function(e) {
      e.preventDefault();
      logoutForm.submit();
    });
  }
});