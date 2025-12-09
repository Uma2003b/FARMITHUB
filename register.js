function handleRegister(event) {
  event.preventDefault();
  
  const role = document.getElementById('role').value;
  const fullname = document.getElementById('fullname').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const phone = document.getElementById('phone').value;
  
  // Accept any credentials
  if (fullname && email) {
    // Store user data without login status
    const userData = {
      role: role || 'user',
      fullname: fullname,
      email: email,
      phone: phone,
      isLoggedIn: false
    };
    
    localStorage.setItem('registeredUser', JSON.stringify(userData));
    
    alert('Account created successfully! Redirecting to login page...');
    
    // Redirect to login.html
    setTimeout(() => {
      window.location.href = 'login.html';
    }, 1000);
  } else {
    alert('Please enter at least name and email');
  }
}

function updateRoleIcon() {
  // Optional: Update role icon based on selection
}

function togglePassword() {
  // Optional: Toggle password visibility
}

function toggleConfirmPassword() {
  // Optional: Toggle confirm password visibility
}

function checkPasswordStrength() {
  // Optional: Check password strength
}

function checkPasswordMatch() {
  // Optional: Check password match
}