function handleLogin(event) {
  event.preventDefault();
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  if (email && password) {
    const userData = {
      email: email,
      fullname: email.split('@')[0] || 'User',
      isLoggedIn: true,
      sessionToken: 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
      loginTime: new Date().toISOString()
    };
    
    localStorage.setItem('currentUser', JSON.stringify(userData));
    sessionStorage.setItem('sessionActive', 'true');
    window.location.href = '/main';
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
