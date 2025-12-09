function handleLogin(event) {
  event.preventDefault();
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  // Accept any credentials
  if (email && password) {
    // Store user data
    const userData = {
      email: email,
      fullname: email.split('@')[0] || 'User',
      isLoggedIn: true
    };
    
    localStorage.setItem('currentUser', JSON.stringify(userData));
    
    // Redirect to main.html
    window.location.href = 'main.html';
  } else {
    alert('Please enter both email and password');
  }
}

function togglePassword() {
  const passwordInput = document.getElementById('password');
  const eyeIcon = document.getElementById('password-eye');
  
  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    eyeIcon.classList.replace('fa-eye', 'fa-eye-slash');
  } else {
    passwordInput.type = 'password';
    eyeIcon.classList.replace('fa-eye-slash', 'fa-eye');
  }
}