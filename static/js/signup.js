  // JavaScript to handle form submission
  document.getElementById('signup-form').addEventListener('submit', function(event) {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirm-password').value;

    if (password !== confirmPassword) {
      alert('Passwords do not match. Please try again.');
      event.preventDefault(); // Prevent form submission if passwords don't match
    } else {
      if (confirm('Are you sure you want to submit the form?')) {
        // Manually submit the form
        this.submit();
      }
    }
  });