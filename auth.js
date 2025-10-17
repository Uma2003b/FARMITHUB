// Authentication System for AgriTech - Updated to use backend API

class AuthManager {
  constructor() {
    this.currentUser = this.getCurrentUser();
  }

  // Set current user session in localStorage
  setCurrentUser(user) {
    try {
      const userSession = {
        id: user.id || '',
        email: user.email,
        fullname: user.fullname || '',
        role: user.role || '',
        loginTime: new Date().toISOString()
      };
      localStorage.setItem('agritech_current_user', JSON.stringify(userSession));
      this.currentUser = userSession;
    } catch (error) {
      console.error('Error setting current user:', error);
    }
  }

  // Get current user session
  getCurrentUser() {
    try {
      const user = localStorage.getItem('agritech_current_user');
      return user ? JSON.parse(user) : null;
    } catch (error) {
      console.error('Error getting current user:', error);
      return null;
    }
  }

  // Check if user is logged in
  isLoggedIn() {
    return this.currentUser !== null;
  }

  // Logout user
  logout() {
    try {
      localStorage.removeItem('agritech_current_user');
      this.currentUser = null;
      return { success: true, message: 'Logged out successfully' };
    } catch (error) {
      console.error('Error during logout:', error);
      return { success: false, message: 'Error during logout' };
    }
  }
}

// Initialize global auth manager
window.authManager = new AuthManager();

// Utility function to show messages
function showAuthMessage(message, type = 'info') {
  const existingMessage = document.querySelector('.auth-message');
  if (existingMessage) {
    existingMessage.remove();
  }

  const messageDiv = document.createElement('div');
  messageDiv.className = `auth-message auth-message-${type}`;
  messageDiv.innerHTML = `
    <div class="auth-message-content">
      <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
      <span>${message}</span>
    </div>
  `;

  messageDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 10000;
    padding: 15px 20px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    animation: slideInRight 0.3s ease-out;
    max-width: 400px;
  `;

  if (type === 'success') {
    messageDiv.style.background = 'linear-gradient(135deg, #4caf50, #45a049)';
  } else if (type === 'error') {
    messageDiv.style.background = 'linear-gradient(135deg, #f44336, #e53935)';
  } else {
    messageDiv.style.background = 'linear-gradient(135deg, #2196f3, #1976d2)';
  }

  document.body.appendChild(messageDiv);

  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.style.animation = 'slideOutRight 0.3s ease-out';
      setTimeout(() => {
        if (messageDiv.parentNode) {
          messageDiv.remove();
        }
      }, 300);
    }
  }, 5000);
}

// Handle login form submission
async function handleLogin(event) {
  event.preventDefault();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  if (!email || !password) {
    showAuthMessage('Please enter email and password', 'error');
    return;
  }

  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const result = await response.json();
    if (result.success) {
      window.authManager.setCurrentUser({ email });
      showAuthMessage('Login successful!', 'success');
      setTimeout(() => {
        window.location.href = '/main';
      }, 1000);
    } else {
      showAuthMessage(result.message || 'Login failed', 'error');
    }
  } catch (error) {
    console.error('Login error:', error);
    showAuthMessage('An error occurred during login', 'error');
  }
}

// Handle register form submission
async function handleRegister(event) {
  event.preventDefault();
  const role = document.getElementById('role').value;
  const fullname = document.getElementById('fullname').value.trim();
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value;

  if (!role || !fullname || !email || !password) {
    showAuthMessage('Please fill in all fields', 'error');
    return;
  }

  try {
    const response = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role, fullname, email, password })
    });
    const result = await response.json();
    if (result.success) {
      window.authManager.setCurrentUser({ email, fullname, role });
      showAuthMessage('Registration successful!', 'success');
      setTimeout(() => {
        window.location.href = '/main';
      }, 1000);
    } else {
      showAuthMessage(result.message || 'Registration failed', 'error');
    }
  } catch (error) {
    console.error('Registration error:', error);
    showAuthMessage('An error occurred during registration', 'error');
  }
}

// Redirect if already logged in
function redirectIfLoggedIn() {
  if (window.authManager.isLoggedIn()) {
    window.location.href = '/main';
  }
}

// Add CSS animations
const authStyles = document.createElement('style');
authStyles.textContent = `
  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100%);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  @keyframes slideOutRight {
    from {
      opacity: 1;
      transform: translateX(0);
    }
    to {
      opacity: 0;
      transform: translateX(100%);
    }
  }

  .auth-message-content {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .auth-message-content i {
    font-size: 1.2rem;
  }
`;
document.head.appendChild(authStyles);
