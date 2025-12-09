// Authentication functionality
class AuthManager {
    constructor() {
        this.currentUser = null;
        this.init();
    }
    
    init() {
        // Check if user is logged in
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) {
            this.currentUser = JSON.parse(savedUser);
            this.updateUI();
        }
    }
    
    login(username, password) {
        // Simple demo login - in production, this would call a real API
        if (username && password) {
            this.currentUser = {
                username: username,
                loginTime: new Date().toISOString()
            };
            localStorage.setItem('currentUser', JSON.stringify(this.currentUser));
            this.updateUI();
            return true;
        }
        return false;
    }
    
    logout() {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
        this.updateUI();
        return {
            success: true,
            message: 'Successfully logged out'
        };
    }
    
    updateUI() {
        const loginBtn = document.querySelector('.login-btn');
        const logoutBtn = document.querySelector('.logout-btn');
        const userInfo = document.querySelector('.user-info');
        
        if (this.currentUser) {
            if (loginBtn) loginBtn.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'block';
            if (userInfo) userInfo.textContent = `Welcome, ${this.currentUser.username}`;
        } else {
            if (loginBtn) loginBtn.style.display = 'block';
            if (logoutBtn) logoutBtn.style.display = 'none';
            if (userInfo) userInfo.textContent = '';
        }
    }
    
    isLoggedIn() {
        return this.currentUser !== null;
    }
    
    getCurrentUser() {
        return this.currentUser;
    }
}

// Initialize auth manager
const authManager = new AuthManager();

// Make auth manager globally accessible
window.authManager = authManager;

// Login form handler
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.querySelector('#username').value;
            const password = document.querySelector('#password').value;
            
            if (authManager.login(username, password)) {
                alert('Login successful!');
                window.location.href = 'http://127.0.0.1:5000/main.html';
            } else {
                alert('Please enter valid credentials');
            }
        });
    }
    
    // Logout button handler
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            authManager.logout();
        });
    }
});