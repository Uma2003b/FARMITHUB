// Theme management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }
    
    init() {
        this.applyTheme(this.currentTheme);
        this.setupThemeToggle();
    }
    
    applyTheme(theme) {
        document.body.setAttribute('data-theme', theme);
        this.currentTheme = theme;
        localStorage.setItem('theme', theme);
        
        // Update theme toggle button
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
            themeToggle.title = `Switch to ${theme === 'light' ? 'dark' : 'light'} theme`;
        }
    }
    
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }
    
    setupThemeToggle() {
        const themeToggle = document.querySelector('.theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }
}

// Dark theme styles
const darkThemeStyles = `
    [data-theme="dark"] {
        --bg-color: #1a1a1a;
        --text-color: #ffffff;
        --card-bg: #2d2d2d;
        --border-color: #404040;
        --primary-color: #4CAF50;
    }
    
    [data-theme="dark"] body {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    [data-theme="dark"] .card {
        background-color: var(--card-bg);
        border-color: var(--border-color);
    }
    
    [data-theme="dark"] input,
    [data-theme="dark"] select,
    [data-theme="dark"] textarea {
        background-color: var(--card-bg);
        color: var(--text-color);
        border-color: var(--border-color);
    }
`;

// Inject dark theme styles
const styleSheet = document.createElement('style');
styleSheet.textContent = darkThemeStyles;
document.head.appendChild(styleSheet);

// Initialize theme manager
document.addEventListener('DOMContentLoaded', function() {
    const themeManager = new ThemeManager();
    
    // Add theme toggle button if it doesn't exist
    if (!document.querySelector('.theme-toggle')) {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'theme-toggle';
        themeToggle.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: none;
            border: 2px solid #ccc;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            font-size: 20px;
            cursor: pointer;
            z-index: 1000;
        `;
        document.body.appendChild(themeToggle);
        themeManager.setupThemeToggle();
    }
});