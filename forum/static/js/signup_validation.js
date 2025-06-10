document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('signupForm');

  form.addEventListener('submit', (e) => {
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Validate username (only letters)
    if (!/^[A-Za-z]+$/.test(username)) {
      alert('Username must contain only letters.');
      e.preventDefault();
      return;
    }

    // Validate email domain
    if (!email.endsWith('@libertycollege.edu.np')) {
      alert('Email must be a @libertycollege.edu.np address.');
      e.preventDefault();
      return;
    }

    // Validate password length
    if (password.length < 6) {
      alert('Password must be at least 6 characters.');
      e.preventDefault();
      return;
    }

    // Validate password match
    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      e.preventDefault();
      return;
    }
  });
});
