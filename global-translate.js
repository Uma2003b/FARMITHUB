// Global Translation System - No separate Telugu files needed
(function() {
  let currentLang = localStorage.getItem('selectedLanguage') || 'en';
  let translateReady = false;

  // Initialize Google Translate on every page
  function initGoogleTranslate() {
    if (typeof google !== 'undefined' && google.translate) {
      new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'en,te',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
      }, 'google_translate_element');
    }
  }

  // Auto-translate on page load if Telugu is selected
  function autoTranslate() {
    if (currentLang === 'te') {
      setTimeout(() => {
        const selectElement = document.querySelector('.goog-te-combo');
        if (selectElement && selectElement.options.length > 1) {
          selectElement.value = 'te';
          selectElement.dispatchEvent(new Event('change'));
          translateReady = true;
        } else if (!translateReady) {
          autoTranslate(); // Retry
        }
      }, 1000);
    }
  }

  // Set up language selector
  function setupLanguageSelector() {
    const selector = document.getElementById('languageSelector');
    if (selector) {
      selector.value = currentLang;
    }
  }

  // Hide Google Translate UI elements
  function hideGoogleTranslateUI() {
    setTimeout(() => {
      const banner = document.querySelector('.goog-te-banner-frame');
      if (banner) banner.style.display = 'none';
      
      const toolbar = document.querySelector('.goog-te-ftab');
      if (toolbar) toolbar.style.display = 'none';
      
      document.body.style.top = '0px';
      
      const combo = document.querySelector('.goog-te-combo');
      if (combo) {
        combo.style.visibility = 'hidden';
        combo.style.position = 'absolute';
        combo.style.left = '-9999px';
      }
    }, 2000);
  }

  // Initialize everything when DOM is ready
  document.addEventListener('DOMContentLoaded', function() {
    // Create Google Translate element if it doesn't exist
    if (!document.getElementById('google_translate_element')) {
      const translateDiv = document.createElement('div');
      translateDiv.id = 'google_translate_element';
      translateDiv.style.display = 'none';
      document.body.appendChild(translateDiv);
    }

    setupLanguageSelector();
    initGoogleTranslate();
    autoTranslate();
    hideGoogleTranslateUI();
  });

  // Global functions
  window.changeLanguage = function() {
    const selector = document.getElementById('languageSelector');
    if (selector) {
      const selectedLang = selector.value;
      localStorage.setItem('selectedLanguage', selectedLang);
      currentLang = selectedLang;
      
      const selectElement = document.querySelector('.goog-te-combo');
      if (selectElement) {
        selectElement.value = selectedLang;
        selectElement.dispatchEvent(new Event('change'));
      }
    }
  };

  window.navigateWithLang = function(page) {
    if (event) event.preventDefault();
    window.location.href = page;
  };

  // Load Google Translate script
  if (!document.querySelector('script[src*="translate.google.com"]')) {
    const script = document.createElement('script');
    script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    document.head.appendChild(script);
  }

  window.googleTranslateElementInit = initGoogleTranslate;
})();