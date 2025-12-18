// Strict Session Management - Prevent unauthorized back button access
(function() {
  const publicPages = ['index.html', 'login.html', 'about.html'];
  
  function isPublicPage() {
    return publicPages.some(page => window.location.pathname.includes(page) || window.location.href.includes(page));
  }

  function isLoggedIn() {
    return !!localStorage.getItem('currentUser');
  }

  function redirectToIndex() {
    window.history.pushState(null, null, window.location.href);
    window.location.replace('/index.html');
  }

  // Check session on page load
  window.addEventListener('load', function() {
    if (!isLoggedIn() && !isPublicPage()) {
      redirectToIndex();
    }
  });

  // Prevent back navigation to protected pages
  window.addEventListener('popstate', function() {
    if (!isLoggedIn() && !isPublicPage()) {
      redirectToIndex();
    }
  });

  // Handle browser back button
  window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
      if (!isLoggedIn() && !isPublicPage()) {
        redirectToIndex();
      }
    }
  });

  // Prevent forward navigation to protected pages
  window.addEventListener('pagehide', function() {
    if (!isLoggedIn() && !isPublicPage()) {
      window.history.pushState(null, null, window.location.href);
    }
  });

  // Clear history and logout
  window.logout = function() {
    localStorage.removeItem('currentUser');
    sessionStorage.clear();
    window.history.pushState(null, null, window.location.href);
    window.location.replace('/index.html');
  };

  // Prevent back on login page after successful login
  window.preventBackAfterLogin = function() {
    window.history.pushState(null, null, window.location.href);
    window.onpopstate = function() {
      window.history.pushState(null, null, window.location.href);
    };
  };
})();
