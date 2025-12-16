// Global Language Management System
class LanguageManager {
  constructor() {
    this.currentLang = localStorage.getItem('selectedLanguage') || 'en';
    this.init();
  }

  init() {
    // Auto-redirect on page load if language mismatch
    this.checkAndRedirect();
    
    // Set up language selector if it exists
    document.addEventListener('DOMContentLoaded', () => {
      this.setupLanguageSelector();
    });
  }

  checkAndRedirect() {
    const currentPage = window.location.pathname.split('/').pop();
    const isTeluguPage = currentPage.includes('_telugu');
    
    if (this.currentLang === 'te' && !isTeluguPage && currentPage !== '') {
      // Should be on Telugu page but on English page
      const teluguPage = currentPage.replace('.html', '_telugu.html');
      window.location.href = teluguPage;
    } else if (this.currentLang === 'en' && isTeluguPage) {
      // Should be on English page but on Telugu page
      const englishPage = currentPage.replace('_telugu.html', '.html');
      window.location.href = englishPage;
    }
  }

  setupLanguageSelector() {
    const selector = document.getElementById('languageSelector');
    if (selector) {
      selector.value = this.currentLang;
    }
  }

  changeLanguage(newLang) {
    this.currentLang = newLang;
    localStorage.setItem('selectedLanguage', newLang);
    
    const currentPage = window.location.pathname.split('/').pop();
    
    if (newLang === 'te') {
      const teluguPage = currentPage.replace('.html', '_telugu.html');
      window.location.href = teluguPage;
    } else {
      const englishPage = currentPage.replace('_telugu.html', '.html');
      window.location.href = englishPage;
    }
  }

  navigateWithLang(page) {
    if (this.currentLang === 'te') {
      const teluguPage = page.replace('.html', '_telugu.html');
      window.location.href = teluguPage;
    } else {
      window.location.href = page;
    }
  }
}

// Initialize global language manager
const langManager = new LanguageManager();

// Global functions for use in HTML
function changeLanguage() {
  const selector = document.getElementById('languageSelector');
  if (selector) {
    langManager.changeLanguage(selector.value);
  }
}

function navigateWithLang(page) {
  event.preventDefault();
  langManager.navigateWithLang(page);
}