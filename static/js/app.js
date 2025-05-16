// Basic JavaScript for the Research Collaboration Platform
document.addEventListener('DOMContentLoaded', function() {
  // Enable Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  });

  // Enable Bootstrap popovers
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  });

  // Handle opportunity card hover effects
  const opportunityCards = document.querySelectorAll('.opportunity-card');
  opportunityCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.classList.add('shadow-lg');
    });
    
    card.addEventListener('mouseleave', function() {
      this.classList.remove('shadow-lg');
    });
  });

  // Profile completeness progress bars
  const progressBars = document.querySelectorAll('.progress-bar');
  progressBars.forEach(bar => {
    const value = parseInt(bar.getAttribute('aria-valuenow'));
    bar.style.width = value + '%';
  });

  // Flash message auto-dismiss
  const flashMessages = document.querySelectorAll('.alert-dismissible');
  flashMessages.forEach(flash => {
    setTimeout(() => {
      const closeButton = flash.querySelector('.btn-close');
      if (closeButton) {
        closeButton.click();
      }
    }, 5000);
  });
});